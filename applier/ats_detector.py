from typing import Optional

def detect_ats(url: str) -> str:
    """Detect ATS type from job URL."""
    url_lower = url.lower()

    if 'boards.greenhouse.io' in url_lower or '/apply' in url_lower and 'greenhouse' in url_lower:
        return 'greenhouse'
    elif 'jobs.lever.co' in url_lower or 'lever.co' in url_lower:
        return 'lever'
    elif 'jobs.ashbyhq.com' in url_lower or 'ashbyhq.com' in url_lower:
        return 'ashby'
    elif 'workday' in url_lower:
        return 'workday'
    elif 'linkedin.com' in url_lower:
        return 'linkedin'
    elif 'indeed' in url_lower:
        return 'indeed'
    elif 'glassdoor' in url_lower:
        return 'glassdoor'

    return 'unknown'
