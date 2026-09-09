from flask import Flask, request, jsonify
from flask_cors import CORS

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from werkzeug.utils import secure_filename

from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity
)

from dotenv import load_dotenv

from models import db, User, Resume

import os
import pdfplumber


# Load environment variables
load_dotenv()


app = Flask(__name__)

CORS(app)


# =========================
# Configuration
# =========================

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///resume.db"

app.config["JWT_SECRET_KEY"] = os.getenv(
    "JWT_SECRET_KEY"
)

# Maximum upload size = 10 MB
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024

UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


# =========================
# Initialize extensions
# =========================

jwt = JWTManager(app)

db.init_app(app)

# AI engine is initialized only when analysis is requested
ats_engine = None


with app.app_context():
    db.create_all()


# =========================
# Error handling
# =========================

@app.errorhandler(413)
def file_too_large(error):

    return jsonify({
        "message": "File is too large. Maximum size is 10 MB."
    }), 413


# =========================
# Home
# =========================

@app.route("/")
def home():

    return {
        "message": "CareerPilot AI Backend Running"
    }


# =========================
# Register
# =========================

@app.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "Invalid request data"
        }), 400

    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    password = data.get("password", "")

    if not name or not email or not password:
        return jsonify({
            "message": "Name, email and password are required"
        }), 400

    existing_user = User.query.filter_by(
        email=email
    ).first()

    if existing_user:
        return jsonify({
            "message": "Email already registered"
        }), 400

    hashed_password = generate_password_hash(
        password
    )

    user = User(
        name=name,
        email=email,
        password=hashed_password
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "User registered successfully"
    })


# =========================
# Login
# =========================

@app.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "Invalid request data"
        }), 400

    email = data.get("email", "").strip()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({
            "message": "Email and password are required"
        }), 400

    user = User.query.filter_by(
        email=email
    ).first()

    if not user:
        return jsonify({
            "message": "User not found"
        }), 404

    if not check_password_hash(
        user.password,
        password
    ):
        return jsonify({
            "message": "Invalid password"
        }), 401

    access_token = create_access_token(
        identity=user.email
    )

    return jsonify({
        "message": "Login successful",
        "token": access_token
    })


# =========================
# Profile
# =========================

@app.route("/profile")
@jwt_required()
def profile():

    current_user = get_jwt_identity()

    return jsonify({
        "email": current_user,
        "message": "Protected route accessed successfully"
    })


# =========================
# Upload Resume
# =========================

@app.route("/upload-resume", methods=["POST"])
@jwt_required()
def upload_resume():

    current_user = get_jwt_identity()

    if "resume" not in request.files:
        return jsonify({
            "message": "No file uploaded"
        }), 400

    file = request.files["resume"]

    if file.filename == "":
        return jsonify({
            "message": "No file selected"
        }), 400

    # Check file extension
    if not file.filename.lower().endswith(".pdf"):
        return jsonify({
            "message": "Only PDF files are allowed"
        }), 400

    # Secure the filename
    filename = secure_filename(
        file.filename
    )

    if not filename:
        return jsonify({
            "message": "Invalid filename"
        }), 400

    # Check actual PDF file signature
    file_header = file.read(4)
    file.seek(0)

    if file_header != b"%PDF":
        return jsonify({
            "message": "Invalid PDF file"
        }), 400

    # Prevent filename collisions between users
    safe_email = secure_filename(
        current_user.split("@")[0]
    )

    filename = f"{safe_email}_{filename}"

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    # Save file
    file.save(filepath)

    # Extract text from PDF
    extracted_text = ""

    try:

        with pdfplumber.open(filepath) as pdf:

            for page in pdf.pages:

                text = page.extract_text()

                if text:
                    extracted_text += text + "\n"

    except Exception:

        # Remove invalid/corrupted PDF
        if os.path.exists(filepath):
            os.remove(filepath)

        return jsonify({
            "message": "Unable to read PDF file"
        }), 400

    # Make sure some text was extracted
    if not extracted_text.strip():

        if os.path.exists(filepath):
            os.remove(filepath)

        return jsonify({
            "message": "Could not extract text from this PDF"
        }), 400

    # Save resume information
    resume = Resume(
        user_email=current_user,
        filename=filename,
        extracted_text=extracted_text
    )

    db.session.add(resume)
    db.session.commit()

    return jsonify({
        "message": "Resume uploaded successfully",
        "filename": filename,
        "characters_extracted": len(extracted_text)
    })


# =========================
# Analyze Resume
# =========================

@app.route("/analyze", methods=["POST"])
@jwt_required()
def analyze_resume():

    global ats_engine

    current_user = get_jwt_identity()

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "Invalid request data"
        }), 400

    job_description = data.get(
        "job_description",
        ""
    ).strip()

    if not job_description:
        return jsonify({
            "message": "Job description is required"
        }), 400

    latest_resume = Resume.query.filter_by(
        user_email=current_user
    ).order_by(
        Resume.id.desc()
    ).first()

    if not latest_resume:
        return jsonify({
            "message": "No resume uploaded"
        }), 404

    try:

        # Import AI engine only when analysis is requested
        if ats_engine is None:

            from ai.ats_engine import ATSEngine

            ats_engine = ATSEngine()

        result = ats_engine.analyze(
            latest_resume.extracted_text,
            job_description
        )

        return jsonify(result)

    except Exception as e:

        print("Analysis error:", e)

        return jsonify({
            "message": "AI analysis is temporarily unavailable. Please try again."
        }), 503


# =========================
# Run application
# =========================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=int(
            os.environ.get(
                "PORT",
                5000
            )
        )
    )