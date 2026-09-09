import json
import os
import spacy
from spacy.matcher import PhraseMatcher

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Get absolute path of current file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Path to skills.json
SKILLS_FILE = os.path.join(
    BASE_DIR,
    "..",
    "data",
    "skills.json"
)


class SkillExtractor:

    def __init__(self):

        # Load skills from JSON
        with open(
            SKILLS_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            self.skills = json.load(file)

        # Create Phrase Matcher
        self.matcher = PhraseMatcher(
            nlp.vocab,
            attr="LOWER"
        )

        # Convert every skill into a spaCy document
        patterns = [
            nlp.make_doc(skill)
            for skill in self.skills
        ]

        # Add all patterns
        self.matcher.add(
            "SKILLS",
            patterns
        )

    def extract(self, text):

        doc = nlp(text)

        matches = self.matcher(doc)

        skills = set()

        for _, start, end in matches:

            skills.add(
                doc[start:end].text
            )

        return sorted(skills)


if __name__ == "__main__":

    sample = """
    Python Flask SQL React Docker AWS

    Developed REST APIs using Flask.
    Worked with Firebase and GitHub.
    Built Machine Learning models using TensorFlow.
    """

    extractor = SkillExtractor()

    print(
        extractor.extract(sample)
    )