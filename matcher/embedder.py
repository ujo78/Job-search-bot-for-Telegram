import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Tuple

class JobEmbedder:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed_text(self, text: str) -> np.ndarray:
        """Embed a text string into a vector."""
        return self.model.encode(text, convert_to_numpy=True)

    def resume_embedding(self, resume_text: str) -> np.ndarray:
        """Create embedding for resume full text."""
        return self.embed_text(resume_text)

    def job_embedding(self, job_title: str, job_description: str) -> np.ndarray:
        """Create embedding for job (title + description)."""
        combined = f"{job_title}\n{job_description}"
        return self.embed_text(combined)

    def cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors."""
        if len(vec1.shape) > 1:
            vec1 = vec1[0]
        if len(vec2.shape) > 1:
            vec2 = vec2[0]

        dot = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return float(dot / (norm1 * norm2))

    def rank_jobs(self, resume_embedding: np.ndarray, jobs: List[dict], top_n: int = 50) -> List[Tuple[dict, float]]:
        """Rank jobs by cosine similarity to resume, return top N."""
        scored_jobs = []

        for job in jobs:
            job_desc = job.get('job_description', '')
            job_title = job.get('title', '')

            if not job_desc or not job_title:
                continue

            job_emb = self.job_embedding(job_title, job_desc)
            score = self.cosine_similarity(resume_embedding, job_emb)
            scored_jobs.append((job, score))

        scored_jobs.sort(key=lambda x: x[1], reverse=True)
        return scored_jobs[:top_n]
