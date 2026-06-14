import aiohttp
from typing import List, Dict
import hashlib

async def fetch_remoteok(max_results: int = 20) -> List[Dict]:
    """Fetch jobs from RemoteOK API (free, no auth)."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://remoteok.com/api') as resp:
                if resp.status == 200:
                    jobs_data = await resp.json()
                    results = []
                    for job in jobs_data[:max_results]:
                        if job.get('url'):
                            results.append({
                                'url': job.get('url'),
                                'url_hash': hashlib.md5(job.get('url', '').encode()).hexdigest(),
                                'title': job.get('position', ''),
                                'company': job.get('company', ''),
                                'location': 'Remote',
                                'job_description': job.get('description', '')[:1000],
                                'ats_type': 'unknown',
                                'source': 'remoteok'
                            })
                    return results
    except Exception as e:
        print(f"RemoteOK error: {e}")
    return []

async def fetch_adzuna(app_id: str, api_key: str, what: str = 'python developer', where: str = 'india', max_results: int = 20) -> List[Dict]:
    """Fetch jobs from Adzuna API (free tier)."""
    if not app_id or not api_key:
        return []

    try:
        async with aiohttp.ClientSession() as session:
            url = f'https://api.adzuna.com/v1/api/jobs/gb/search/1'
            params = {
                'app_id': app_id,
                'app_key': api_key,
                'what': what,
                'where': where,
                'results_per_page': max_results
            }
            async with session.get(url, params=params) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    results = []
                    for job in data.get('results', []):
                        results.append({
                            'url': job.get('redirect_url', ''),
                            'url_hash': hashlib.md5(job.get('redirect_url', '').encode()).hexdigest(),
                            'title': job.get('title', ''),
                            'company': job.get('company', {}).get('display_name', ''),
                            'location': job.get('location', {}).get('display_name', ''),
                            'job_description': job.get('description', '')[:1000],
                            'ats_type': 'unknown',
                            'source': 'adzuna'
                        })
                    return results
    except Exception as e:
        print(f"Adzuna error: {e}")
    return []

async def fetch_jobicy(max_results: int = 20) -> List[Dict]:
    """Fetch jobs from Jobicy API (free, no auth, remote focus)."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://jobicy.com/api/v2/remote-jobs', params={'count': max_results}) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    results = []
                    for job in data.get('jobs', []):
                        results.append({
                            'url': job.get('url', ''),
                            'url_hash': hashlib.md5(job.get('url', '').encode()).hexdigest(),
                            'title': job.get('jobTitle', ''),
                            'company': job.get('companyName', ''),
                            'location': 'Remote',
                            'job_description': job.get('jobDescription', '')[:1000],
                            'ats_type': 'unknown',
                            'source': 'jobicy'
                        })
                    return results
    except Exception as e:
        print(f"Jobicy error: {e}")
    return []
