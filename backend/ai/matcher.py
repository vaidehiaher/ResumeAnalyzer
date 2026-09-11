from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class ResumeMatcher:

    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            stop_words="english"
        )

    def similarity(
        self,
        resume_text,
        job_description
    ):

        documents = [
            resume_text,
            job_description
        ]

        embeddings = self.vectorizer.fit_transform(
            documents
        )

        score = cosine_similarity(
            embeddings[0:1],
            embeddings[1:2]
        )[0][0]

        return round(
            float(score) * 100,
            2
        )


if __name__ == "__main__":

    resume = """
    Python
    Flask
    SQL
    JWT
    React
    Docker
    """

    job = """
    Looking for Python Flask Developer.

    Skills:

    Python
    Flask
    Docker
    SQL
    Git
    """

    matcher = ResumeMatcher()

    print(
        matcher.similarity(
            resume,
            job
        )
    )