from jobspy import scrape_jobs
from typing import List, Dict
import hashlib

async def scrape_jobspy(search_term: str, location: str, country: str, max_results: int = 50) -> List[Dict]:
    """Scrape jobs from Indeed, LinkedIn, Glassdoor, Naukri using JobSpy."""
    try:
        jobs = scrape_jobs(
            site_name=["indeed", "linkedin", "glassdoor", "naukri"],
            search_term=search_term,
            location=location,
            results_wanted=max_results,
            hours_old=24,
            country_indeed=country
        )

        results = []
        for job in jobs:
            url_hash = hashlib.md5(str(job.get('job_url', '')).encode()).hexdigest()
            results.append({
                'url': job.get('job_url', ''),
                'url_hash': url_hash,
                'title': job.get('job_title', ''),
                'company': job.get('company', ''),
                'location': job.get('location', ''),
                'job_description': job.get('job_description', ''),
                'ats_type': detect_ats_from_url(job.get('job_url', '')),
                'source': job.get('site_name', 'unknown')
            })
        return results
    except Exception as e:
        print(f"JobSpy error: {e}")
        return []

def detect_ats_from_url(url: str) -> str:
    """Simple ATS detection from URL."""
    if 'greenhouse' in url.lower() or 'boards.greenhouse' in url:
        return 'greenhouse'
    elif 'lever' in url.lower() or 'jobs.lever' in url:
        return 'lever'
    elif 'ashby' in url.lower() or 'jobs.ashbyhq' in url:
        return 'ashby'
    elif 'workday' in url.lower():
        return 'workday'
    elif 'linkedin' in url.lower():
        return 'linkedin'
    return 'unknown'
