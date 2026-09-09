import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import errors


load_dotenv()


# -----------------------------------------
# Gemini API Setup
# -----------------------------------------

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set")


client = genai.Client(
    api_key=api_key
)


# -----------------------------------------
# Generate AI Feedback
# -----------------------------------------

def generate_ai_feedback(
    resume_text,
    job_description,
    matched_skills,
    missing_skills,
    match_score
):

    prompt = f"""
You are an expert ATS resume analyzer and career coach.

Analyze the candidate's resume against the target job description.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

MATCH SCORE:
{match_score}%

MATCHED SKILLS:
{", ".join(matched_skills)}

MISSING SKILLS:
{", ".join(missing_skills)}

Provide useful and personalized feedback.

Return ONLY valid JSON in exactly this structure:

{{
    "summary": "A concise summary of how well the candidate fits the role.",
    "strengths": [
        "Strength 1",
        "Strength 2",
        "Strength 3"
    ],
    "weaknesses": [
        "Weakness 1",
        "Weakness 2",
        "Weakness 3"
    ],
    "suggestions": [
        "Suggestion 1",
        "Suggestion 2",
        "Suggestion 3"
    ]
}}

Important:
- Base the feedback only on the resume and job description.
- Do not invent experience or skills.
- Mention specific technologies or experience when relevant.
- Suggestions should be actionable.
- Keep each item concise.
"""


    # -----------------------------------------
    # Models
    # -----------------------------------------

    models = [
        "gemini-3.5-flash-lite",
        "gemini-3.6-flash"
    ]


    # -----------------------------------------
    # Try each model
    # -----------------------------------------

    for model in models:

        max_retries = 3

        for attempt in range(max_retries):

            try:

                print(
                    f"Trying Gemini model: {model}"
                )

                response = client.models.generate_content(

                    model=model,

                    contents=prompt

                )

                print(
                    f"Gemini request successful: {model}"
                )

                return response.text


            except errors.APIError as e:

                # ---------------------------------
                # Temporary Gemini errors
                # ---------------------------------

                if e.code in [
                    429,
                    500,
                    502,
                    503,
                    504
                ]:

                    if attempt < max_retries - 1:

                        wait_time = 2 ** attempt

                        print(
                            f"Gemini {model} temporarily "
                            f"unavailable."
                        )

                        print(
                            f"Retrying in "
                            f"{wait_time} seconds..."
                        )

                        time.sleep(
                            wait_time
                        )

                    else:

                        print(
                            f"Gemini model {model} "
                            f"failed after retries."
                        )

                        # Try the next model
                        break


                else:

                    # ---------------------------------
                    # Permanent error
                    # ---------------------------------

                    raise


    # -----------------------------------------
    # All models failed
    # -----------------------------------------

    raise RuntimeError(
        "Gemini AI service is temporarily "
        "unavailable. Please try again later."
    )