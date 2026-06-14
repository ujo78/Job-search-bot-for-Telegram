#!/usr/bin/env python
"""
Quick setup script to initialize the job search bot with user input.
Run this before running bot/main.py for the first time.
"""

import os
import subprocess
from pathlib import Path

def main():
    print("=" * 60)
    print("Job Search Bot — Quick Setup")
    print("=" * 60)
    print()

    # Check if .env exists
    if os.path.exists(".env"):
        print("✅ .env file already exists")
        use_existing = input("Use existing .env? (y/n): ").lower().strip()
        if use_existing != 'n':
            return

    # Get Telegram token
    print()
    print("1️⃣  Telegram Bot Token")
    print("   Get from: https://t.me/botfather")
    print("   Commands: /start → /newbot → follow prompts → copy token")
    telegram_token = input("   Enter TELEGRAM_BOT_TOKEN: ").strip()

    # Get Anthropic API key
    print()
    print("2️⃣  Anthropic API Key")
    print("   Get from: https://console.anthropic.com/account/keys")
    print("   (Required for resume matching + cover letters)")
    anthropic_key = input("   Enter ANTHROPIC_API_KEY: ").strip()

    # Get Adzuna keys (optional)
    print()
    print("3️⃣  Adzuna API Keys (Optional)")
    print("   Get from: https://developer.adzuna.com/")
    print("   (Leave empty to skip)")
    adzuna_app_id = input("   ADZUNA_APP_ID (optional): ").strip()
    adzuna_api_key = input("   ADZUNA_API_KEY (optional): ").strip()

    # Get search preferences
    print()
    print("4️⃣  Job Search Preferences")
    search_keywords = input("   Job title to search for (default: Software Engineer): ").strip() or "Software Engineer"
    location = input("   Location to search (default: India): ").strip() or "India"
    country = input("   Country code (default: india): ").strip().lower() or "india"
    search_interval = input("   Search interval in hours (default: 6): ").strip() or "6"

    # Create .env file
    print()
    print("💾 Creating .env file...")
    env_content = f"""TELEGRAM_BOT_TOKEN={telegram_token}
ANTHROPIC_API_KEY={anthropic_key}
ADZUNA_APP_ID={adzuna_app_id}
ADZUNA_API_KEY={adzuna_api_key}

SEARCH_KEYWORDS={search_keywords}
LOCATION={location}
COUNTRY={country}
SEARCH_INTERVAL_HOURS={search_interval}
MAX_RESULTS_PER_RUN=50
MIN_MATCH_SCORE=6

DB_PATH=job_search.db
RESUME_DIR=resumes
SCREENSHOTS_DIR=screenshots
"""

    with open(".env", "w") as f:
        f.write(env_content)

    print("✅ .env file created")

    # Install dependencies
    print()
    print("📦 Installing dependencies...")
    try:
        subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependencies installed")
    except subprocess.CalledProcessError:
        print("❌ Dependency installation failed. Try: pip install -r requirements.txt")
        return

    # Install Playwright browsers
    print()
    print("🌐 Installing Playwright browsers...")
    try:
        subprocess.run(["python", "-m", "playwright", "install", "chromium"], check=True)
        print("✅ Playwright browsers installed")
    except subprocess.CalledProcessError:
        print("❌ Playwright installation failed. Try: python -m playwright install chromium")
        return

    # Create directories
    print()
    print("📁 Creating directories...")
    os.makedirs("resumes", exist_ok=True)
    os.makedirs("screenshots", exist_ok=True)
    print("✅ Directories created")

    # Final instructions
    print()
    print("=" * 60)
    print("✅ Setup Complete!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Open Telegram and find your bot (@YourBotName)")
    print("2. Send /start to initialize")
    print("3. Send /resume and upload your PDF resume")
    print("4. Send /search to find matching jobs")
    print()
    print("To run the bot:")
    print("   python bot/main.py")
    print()
    print("For help, see README.md or run:")
    print("   python bot/main.py --help")

if __name__ == "__main__":
    main()
