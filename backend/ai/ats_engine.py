import json

from ai.parser import parse_resume
from ai.matcher import ResumeMatcher
from ai.skill_extractor import SkillExtractor
from services.ai_service import generate_ai_feedback


class ATSEngine:

    def __init__(self):

        self.matcher = ResumeMatcher()
        self.skill_extractor = SkillExtractor()

    def analyze(self, resume_text, job_description):

        # -----------------------------------------
        # 1. Parse Resume
        # -----------------------------------------

        resume = parse_resume(resume_text)

        # -----------------------------------------
        # 2. Extract Skills
        # -----------------------------------------

        resume_skills = self.skill_extractor.extract(
            resume_text
        )

        job_skills = self.skill_extractor.extract(
            job_description
        )

        # -----------------------------------------
        # 3. Find Matched Skills
        # -----------------------------------------

        matched_skills = sorted(
            list(
                set(resume_skills)
                &
                set(job_skills)
            )
        )

        # -----------------------------------------
        # 4. Find Missing Skills
        # -----------------------------------------

        missing_skills = sorted(
            list(
                set(job_skills)
                -
                set(resume_skills)
            )
        )

        # -----------------------------------------
        # 5. Calculate Semantic Match Score
        # -----------------------------------------

        match_score = self.matcher.similarity(
            resume_text,
            job_description
        )

        # -----------------------------------------
        # 6. Calculate ATS Score
        # -----------------------------------------

        ats_score = self.calculate_ats(
            resume,
            match_score,
            len(matched_skills),
            len(missing_skills)
        )

        # -----------------------------------------
        # 7. Generate AI Feedback using Gemini
        # -----------------------------------------

        ai_feedback_text = generate_ai_feedback(
            resume_text=resume_text,
            job_description=job_description,
            matched_skills=matched_skills,
            missing_skills=missing_skills,
            match_score=match_score
        )

        # -----------------------------------------
        # 8. Convert Gemini JSON to Python Dictionary
        # -----------------------------------------

        ai_feedback = self.parse_ai_feedback(
            ai_feedback_text
        )

        # -----------------------------------------
        # 9. Return Complete Analysis
        # -----------------------------------------

        return {

            "ats_score": ats_score,

            "match_score": match_score,

            "matched_skills": matched_skills,

            "missing_skills": missing_skills,

            "summary": ai_feedback.get(
                "summary",
                ""
            ),

            "strengths": ai_feedback.get(
                "strengths",
                []
            ),

            "weaknesses": ai_feedback.get(
                "weaknesses",
                []
            ),

            "suggestions": ai_feedback.get(
                "suggestions",
                []
            )
        }

    # -----------------------------------------
    # AI FEEDBACK JSON PARSER
    # -----------------------------------------

    def parse_ai_feedback(self, ai_feedback_text):

        try:

            if not ai_feedback_text:
                raise ValueError(
                    "Empty Gemini response"
                )

            # Convert response to string
            cleaned_feedback = str(
                ai_feedback_text
            ).strip()

            # Remove ```json code fence
            if cleaned_feedback.startswith(
                "```json"
            ):

                cleaned_feedback = (
                    cleaned_feedback[7:]
                )

            # Remove generic ``` code fence
            elif cleaned_feedback.startswith(
                "```"
            ):

                cleaned_feedback = (
                    cleaned_feedback[3:]
                )

            # Remove ending ```
            if cleaned_feedback.endswith(
                "```"
            ):

                cleaned_feedback = (
                    cleaned_feedback[:-3]
                )

            cleaned_feedback = (
                cleaned_feedback.strip()
            )

            # Convert JSON string to dictionary
            ai_feedback = json.loads(
                cleaned_feedback
            )

            # Make sure Gemini returned an object
            if not isinstance(
                ai_feedback,
                dict
            ):
                raise ValueError(
                    "Gemini response is not a JSON object"
                )

            # Make sure expected fields exist
            return {
                "summary": ai_feedback.get(
                    "summary",
                    ""
                ),

                "strengths": ai_feedback.get(
                    "strengths",
                    []
                ),

                "weaknesses": ai_feedback.get(
                    "weaknesses",
                    []
                ),

                "suggestions": ai_feedback.get(
                    "suggestions",
                    []
                )
            }

        except (
            json.JSONDecodeError,
            TypeError,
            ValueError
        ):

            # Safe fallback if Gemini returns
            # invalid or unexpected JSON

            return {
                "summary": (
                    "Unable to generate AI feedback."
                ),

                "strengths": [],

                "weaknesses": [],

                "suggestions": []
            }

    # -----------------------------------------
    # ATS SCORE CALCULATION
    # -----------------------------------------

    def calculate_ats(
        self,
        resume,
        match_score,
        matched,
        missing
    ):

        score = 40

        # Semantic similarity contribution
        score += match_score * 0.4

        # Matched skills contribution
        score += matched * 2

        # Missing skills penalty
        score -= missing

        # Resume section bonuses
        if resume["projects"]:
            score += 8

        if resume["experience"]:
            score += 8

        if resume["certifications"]:
            score += 4

        # Keep score between 0 and 100
        return round(
            min(max(score, 0), 100),
            2
        )