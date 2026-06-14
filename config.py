import os
from dotenv import load_dotenv

load_dotenv()

# Telegram
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")

# Anthropic
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

# Job search
SEARCH_KEYWORDS = os.getenv("SEARCH_KEYWORDS", "Software Engineer")
LOCATION = os.getenv("LOCATION", "India")
COUNTRY = os.getenv("COUNTRY", "india")
SEARCH_INTERVAL_HOURS = int(os.getenv("SEARCH_INTERVAL_HOURS", "6"))
MAX_RESULTS_PER_RUN = int(os.getenv("MAX_RESULTS_PER_RUN", "50"))
MIN_MATCH_SCORE = float(os.getenv("MIN_MATCH_SCORE", "6"))

# Free API keys
ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID", "")
ADZUNA_API_KEY = os.getenv("ADZUNA_API_KEY", "")

# Database
DB_PATH = os.getenv("DB_PATH", "job_search.db")

# Storage
RESUME_DIR = os.getenv("RESUME_DIR", "resumes")
SCREENSHOTS_DIR = os.getenv("SCREENSHOTS_DIR", "screenshots")

# Ensure directories exist
os.makedirs(RESUME_DIR, exist_ok=True)
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
