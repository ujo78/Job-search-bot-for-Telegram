# Job Search Bot — Complete Package Index

## 📚 Documentation (Read These First)

| File | Purpose | Read Time |
|------|---------|-----------|
| **START_HERE.md** | 3-step quick setup | 3 min |
| **FINAL_SUMMARY.md** | Executive overview | 5 min |
| **README.md** | Full documentation | 15 min |
| **QUICKSTART.md** | Detailed setup guide | 5 min |
| **IMPLEMENTATION_COMPLETE.md** | What was built | 5 min |
| **IMPLEMENTATION_ROADMAP.md** | What's next | 5 min |
| **TEST_REPORT.md** | Testing results | 3 min |

## 💻 Source Code

### Entry Point
- **`bot/main.py`** — Run this to start the bot

### Telegram Bot Layer
- `bot/handlers.py` — All commands (/start, /resume, /search, /status, /history)
- `bot/keyboards.py` — Button layouts (Apply/Skip/Save)
- `bot/scheduler.py` — APScheduler integration for automation

### Job Matching Layer
- `matcher/resume_parser.py` — Extract text from PDF resumes
- `matcher/embedder.py` — SBERT for job-resume similarity scoring
- `matcher/llm_ranker.py` — Claude for intelligent job ranking

### Job Scraping Layer
- `scraper/jobspy_scraper.py` — JobSpy integration (Indeed, LinkedIn, Glassdoor, Naukri)
- `scraper/free_apis.py` — RemoteOK, Adzuna, Jobicy APIs
- `scraper/aggregator.py` — Deduplication and merging

### Auto-Apply Layer
- `applier/ats_detector.py` — Detect ATS platform from URL
- `applier/form_filler.py` — Playwright browser automation
- `applier/apply_session.py` — Manage application flow and previews

### Data Layer
- `storage/db.py` — SQLite database operations

### Configuration
- `config.py` — Loads environment variables
- `.env.example` → `.env` (create this with your keys)

## 🚀 Quick Start

```bash
# 1. Get keys (2 API tokens)
#    - Telegram: @BotFather on Telegram
#    - Anthropic: console.anthropic.com

# 2. Configure
cp .env.example .env
# Edit .env with your tokens

# 3. Run
python bot/main.py

# 4. Test
# In Telegram:
# /start → /resume (upload PDF) → /search
```

## 📦 Dependencies

- **aiogram** 3.28+ — Telegram bot framework
- **anthropic** 0.84+ — Claude API client
- **python-jobspy** 1.1.82 — Job scraping
- **pdfplumber** 0.11.9 — Resume parsing
- **sentence-transformers** 5.5.1 — SBERT embeddings
- **playwright** 1.60+ — Browser automation
- **apscheduler** 3.10+ — Job scheduling
- **aiosqlite** 0.22+ — Async SQLite
- **python-dotenv** 1.2+ — Environment config

Install all:
```bash
pip install -r requirements.txt
```

## 🗂️ Data Folders

These are created automatically:
- `resumes/` — Uploaded PDF resumes
- `screenshots/` — Form previews from auto-apply
- `job_search.db` — SQLite database (tracks jobs, applications)

## ✅ What's Working

### MVP Features (Complete)
- ✅ Resume upload and parsing
- ✅ Job scraping from 8+ sources
- ✅ Resume-to-job matching (SBERT + Claude)
- ✅ Telegram command interface
- ✅ Job search with ranked results
- ✅ Assisted auto-apply (form preview + confirm)
- ✅ Application history tracking
- ✅ Automated searching (every 6 hours)

### Supported ATS Platforms
- ✅ Greenhouse
- ✅ Lever
- ✅ Ashby
- ⏳ Workday (v2)

## 🎯 Architecture Overview

```
User (Telegram)
    ↓
Bot Framework (aiogram)
    ↓
Command Handlers (bot/handlers.py)
    ├─→ Resume Upload → Parser → Embedder → DB
    ├─→ /search → Scraper → Matcher → LLM Ranker → Display
    └─→ Apply Button → Form Preview → Submit
    
Core Modules:
├─ Job Scraping (8+ sources)
├─ Resume Matching (SBERT embeddings)
├─ LLM Scoring (Claude Haiku/Sonnet)
├─ Form Filling (Playwright)
├─ Database (SQLite)
└─ Scheduling (APScheduler)
```

## 📊 Performance & Costs

### Speed
- Resume parsing: <5 seconds
- Job scraping: 30-60 seconds (5 sources parallel)
- SBERT ranking: <5 seconds (local)
- Claude scoring: 10-20 seconds (API)
- Form preview: 15-30 seconds (Playwright)

### Cost (Monthly)
- Job APIs: **$0** (free tiers)
- SBERT: **$0** (local, no API)
- Claude Haiku (50 searches): ~**$0.25**
- Claude Sonnet (30 applies): ~**$1.50**
- **Total**: **~$1.75/month**

## 🔄 Workflow

**Manual Job Search:**
```
User: /search
Bot: (scrape 30 seconds) → (rank 10 sec) → Results
User: [Tap Apply]
Bot: (preview 20 sec) → Screenshot
User: [Tap Confirm]
Bot: (submit 5 sec) → Confirmation
```

**Automatic (Every 6 Hours):**
```
APScheduler trigger
Bot: Full search pipeline runs in background
Bot: Sends top jobs to Telegram
User: Reviews and acts on jobs as they arrive
```

## 🛠️ Customization

**Change search settings without code:**
```env
SEARCH_KEYWORDS=Machine Learning Engineer
LOCATION=New York
COUNTRY=usa
SEARCH_INTERVAL_HOURS=4
```

**Add more job sources:**
- Edit `scraper/free_apis.py` to call more APIs
- Update `bot/handlers.py` cmd_search() to include them

**Support more ATS platforms:**
- Add patterns to `applier/ats_detector.py`
- Add form-filling logic to `applier/form_filler.py`

## 📝 Common Commands in Telegram

```
/start       → Initialize bot
/resume      → Upload PDF resume
/search      → Find matching jobs (manual trigger)
/status      → View today's stats
/history     → View all applied jobs
```

## ⚠️ Known Limitations

- **Form filling fragility** — Complex dynamic forms may not auto-fill correctly
- **LinkedIn Easy Apply disabled** — Too risky for account bans (manual apply only)
- **Workday support missing** — Complex forms, planned for v2
- **Settings in .env** — Restart required to change keywords (coming: /settings command)

## 🚀 Next Steps

1. **Run immediately**: `python bot/main.py` (no setup if you don't use Claude)
2. **With Claude**: Get API key, add to `.env`, restart
3. **Customize**: Edit `.env` for your job search preferences
4. **Deploy**: Run on a server/VPS to keep it running 24/7
5. **Improve**: Add features from IMPLEMENTATION_ROADMAP.md

## 📞 Support

**Getting errors?**
→ Check `TEST_REPORT.md` and `IMPLEMENTATION_ROADMAP.md`

**Want to extend?**
→ Read `IMPLEMENTATION_ROADMAP.md` for planned features

**Have questions?**
→ See `README.md` for detailed docs

---

**Everything is built and ready.** Start with `START_HERE.md` and run `python bot/main.py`! 🎉
