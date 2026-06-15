# Job Search Bot — Build Complete ✅

Your complete job search automation system is ready. Here's what was built:

## What You Have

A **full-stack Python application** that:
- 📄 Parses your PDF resume and computes skill embeddings
- 🔍 Searches **8+ job boards** simultaneously (Indeed, LinkedIn, Glassdoor, Naukri, RemoteOK, Adzuna, Jobicy)
- 🧠 Ranks jobs using SBERT embeddings + Claude LLM (Haiku for speed, Sonnet for quality)
- 📱 Delivers digests to **Telegram** with action buttons (Apply / Skip / Save)
- 🤖 Pre-fills job application forms using Playwright (Greenhouse, Lever, Ashby ATS)
- 🔄 Runs **automatically every 6 hours** via APScheduler
- 💾 Tracks jobs, applications, and history in SQLite

## Quick Start

### 1. First Run (Interactive Setup)
```bash
cd "Desktop/job search bot"
python setup.py
```
This will prompt you for:
- Telegram bot token (get from @BotFather on Telegram)
- Anthropic API key (get from console.anthropic.com)
- Job search preferences (title, location, interval)

### 2. Start the Bot
```bash
python bot/main.py
```
Bot will start polling Telegram and initialize the database.

### 3. Use in Telegram
1. Find your bot and send `/start`
2. Send `/resume` and upload your PDF
3. Send `/search` to find jobs
4. Tap buttons: ✅ Apply, ⏭️ Skip, 💾 Save
5. For Apply: review form preview, tap Confirm & Submit

## File Structure

```
job-search-bot/
├── README.md                 # Full documentation
├── requirements.txt          # Python dependencies
├── setup.py                  # Interactive setup script
├── config.py                 # Config from .env
│
├── bot/
│   ├── main.py               # Entry point
│   ├── handlers.py           # Telegram commands
│   ├── scheduler.py          # Job scheduling
│   └── keyboards.py          # Button layouts
│
├── matcher/
│   ├── resume_parser.py      # PDF → structured JSON
│   ├── embedder.py           # SBERT ranking
│   └── llm_ranker.py         # Claude scoring & cover letters
│
├── scraper/
│   ├── jobspy_scraper.py     # JobSpy integration
│   ├── free_apis.py          # RemoteOK, Adzuna, Jobicy
│   └── aggregator.py         # Dedup & merge
│
├── applier/
│   ├── ats_detector.py       # Detect ATS type
│   ├── form_filler.py        # Playwright automation
│   └── apply_session.py      # Apply workflow
│
└── storage/
    └── db.py                 # SQLite schema & queries
```

## Key Features

### ✅ Implemented
- Resume parsing (pdfplumber)
- Job scraping from 8+ sources
- Resume-to-job matching with embeddings
- LLM-based ranking and scoring
- Claude cover letter generation
- Telegram bot with inline buttons
- Assisted auto-apply (form pre-fill + human confirm)
- SQLite persistence
- Scheduled searches (6-hour intervals)
- Job deduplication

### ⏭️ Future Improvements (v2+)
- Fully autonomous applying (once success rate is proven)
- Workday form automation (complex, low-priority)
- Resume versioning (tailor per job type)
- Web dashboard for job search UI
- Email digest option
- Proxy rotation for high-volume scraping

## Costs

| Component | Cost/Run |
|-----------|----------|
| Job scraping (all APIs) | **FREE** |
| Resume embeddings (local SBERT) | **FREE** |
| Haiku scoring (50 jobs) | ~$0.005 |
| Sonnet cover letter (per apply) | ~$0.05 |
| **Monthly (~180 searches, 30 applies)** | **~$2–3** |

## Customization

All settings in `.env`:
```env
SEARCH_KEYWORDS=Software Engineer
LOCATION=India
COUNTRY=india
SEARCH_INTERVAL_HOURS=6
MIN_MATCH_SCORE=6
```

## Troubleshooting

**Bot doesn't respond?**
→ Check `TELEGRAM_BOT_TOKEN` in `.env`

**Resume parsing fails?**
→ Ensure it's a `.pdf` (not image-based PDF)

**No jobs found?**
→ Check `SEARCH_KEYWORDS` and internet connection

**Claude API errors?**
→ Verify `ANTHROPIC_API_KEY` has credits remaining

See **README.md** for detailed docs and advanced config.

## Next Steps

1. ✅ Run `python setup.py` to configure your bot
2. ✅ Run `python bot/main.py` to start
3. ✅ Upload resume via `/resume` in Telegram
4. ✅ Check job digest with `/search`
5. ✅ Try apply flow on a job you like

Good luck with your job search! 🚀
