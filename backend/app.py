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

from models import db, User, Resume

import os
import pdfplumber

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///resume.db"

app.config["JWT_SECRET_KEY"] = "careerpilot-secret-key"

UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

jwt = JWTManager(app)

# Hugging Face Model
model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return {
        "message": "CareerPilot AI Backend Running"
    }


@app.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    hashed_password = generate_password_hash(
        data["password"]
    )

    user = User(
        name=data["name"],
        email=data["email"],
        password=hashed_password
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "User registered successfully"
    })


@app.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    user = User.query.filter_by(
        email=data["email"]
    ).first()

    if not user:
        return jsonify({
            "message": "User not found"
        }), 404

    if not check_password_hash(
        user.password,
        data["password"]
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


@app.route("/profile")
@jwt_required()
def profile():

    current_user = get_jwt_identity()

    return jsonify({
        "email": current_user,
        "message": "Protected route accessed successfully"
    })


@app.route("/upload-resume", methods=["POST"])
@jwt_required()
def upload_resume():

    current_user = get_jwt_identity()

    if "resume" not in request.files:
        return jsonify({
            "message": "No file uploaded"
        }), 400

    file = request.files["resume"]

    filename = secure_filename(
        file.filename
    )

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    file.save(filepath)

    extracted_text = ""

    with pdfplumber.open(filepath) as pdf:

        for page in pdf.pages:

            text = page.extract_text()

            if text:
                extracted_text += text + "\n"

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


@app.route("/match-job", methods=["POST"])
@jwt_required()
def match_job():

    current_user = get_jwt_identity()

    data = request.get_json()

    job_description = data.get(
        "job_description",
        ""
    )

    latest_resume = Resume.query.filter_by(
        user_email=current_user
    ).order_by(
        Resume.id.desc()
    ).first()

    if not latest_resume:
        return jsonify({
            "message": "No resume found"
        }), 404

    resume_text = latest_resume.extracted_text

    resume_embedding = model.encode(
        [resume_text]
    )

    job_embedding = model.encode(
        [job_description]
    )

    similarity = cosine_similarity(
        resume_embedding,
        job_embedding
    )[0][0]

    match_score = float(
        round(
            float(similarity) * 100,
            2
        )
    )

    return jsonify({
        "match_score": match_score
    })


@app.route("/users")
def users():

    all_users = User.query.all()

    result = []

    for user in all_users:
        result.append({
            "id": user.id,
            "name": user.name,
            "email": user.email
        })

    return jsonify(result)


@app.route("/delete-all")
def delete_all():

    User.query.delete()

    db.session.commit()

    return {
        "message": "All users deleted"
    }


if __name__ == "__main__":
    app.run(
        debug=True,
        use_reloader=False
    )