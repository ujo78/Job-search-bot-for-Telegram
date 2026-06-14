from typing import List, Dict
from difflib import SequenceMatcher

async def aggregate_jobs(all_jobs: List[List[Dict]]) -> List[Dict]:
    """Dedup jobs by URL hash and title+company fuzzy match, return deduplicated list."""
    seen_urls = set()
    seen_jobs = []
    final_jobs = []

    # Flatten all job sources
    for job_list in all_jobs:
        for job in job_list:
            url_hash = job.get('url_hash', '')

            # Skip if we've seen this URL
            if url_hash in seen_urls:
                continue

            # Check for fuzzy match with existing jobs (same title + company)
            title = job.get('title', '').lower().strip()
            company = job.get('company', '').lower().strip()

            is_duplicate = False
            for seen_job in seen_jobs:
                seen_title = seen_job.get('title', '').lower().strip()
                seen_company = seen_job.get('company', '').lower().strip()

                title_similarity = SequenceMatcher(None, title, seen_title).ratio()
                company_similarity = SequenceMatcher(None, company, seen_company).ratio()

                if title_similarity > 0.85 and company_similarity > 0.85:
                    is_duplicate = True
                    break

            if not is_duplicate:
                seen_urls.add(url_hash)
                seen_jobs.append(job)
                final_jobs.append(job)

    return final_jobs
