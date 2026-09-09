from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class ResumeMatcher:

    def __init__(self):

        self.model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

    def similarity(
        self,
        resume_text,
        job_description
    ):

        embeddings = self.model.encode(
            [
                resume_text,
                job_description
            ]
        )

        score = cosine_similarity(
            [embeddings[0]],
            [embeddings[1]]
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

    Skills

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