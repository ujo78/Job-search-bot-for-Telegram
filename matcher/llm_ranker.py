from anthropic import Anthropic
from typing import List, Dict, Tuple
import json

class LLMRanker:
    def __init__(self, api_key: str):
        self.client = Anthropic(api_key=api_key)

    def score_jobs(self, resume_text: str, jobs: List[Dict]) -> List[Dict]:
        """Score top ~50 jobs using Claude Haiku for bulk ranking."""
        job_summaries = []
        for i, job in enumerate(jobs):
            job_summaries.append(f"{i+1}. {job.get('title', 'Unknown')} at {job.get('company', 'Unknown')} in {job.get('location', 'Unknown')}")

        prompt = f"""You are a job-resume matching expert. Given a resume and a list of job postings, score each job's fit on a scale of 0-10 (where 10 is perfect fit).

RESUME (key details):
{resume_text[:2000]}

JOBS TO SCORE:
{chr(10).join(job_summaries)}

Respond ONLY as valid JSON array, no other text. Each element must have "index" (1-based), "score" (0-10), and "reason" (1 sentence max). Example:
[
  {{"index": 1, "score": 8, "reason": "Strong Python/backend match"}},
  {{"index": 2, "score": 4, "reason": "Requires DevOps experience not in resume"}}
]"""

        response = self.client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )

        text = response.content[0].text.strip()
        try:
            scores = json.loads(text)
            return scores
        except json.JSONDecodeError:
            # Fallback: return all jobs with score 5
            return [{"index": i+1, "score": 5, "reason": "Scoring service error"} for i in range(len(jobs))]

    def generate_cover_letter(self, resume_text: str, job_title: str, company: str, job_description: str) -> str:
        """Generate a tailored cover letter using Claude Sonnet."""
        prompt = f"""Write a brief, professional cover letter (3-4 paragraphs, ~200 words) for the following position.

POSITION: {job_title} at {company}
JOB DESCRIPTION: {job_description[:1500]}

RESUME SUMMARY:
{resume_text[:1500]}

Write a compelling cover letter that highlights relevant experience and skills. Be specific and personable."""

        response = self.client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}]
        )

        return response.content[0].text.strip()
