# Job Search Automation Bot

An intelligent job search automation system that scans job boards for opportunities matching your resume, delivers digests via Telegram, and supports assisted job applications.

## Features

✅ **Resume-Driven Matching** — Upload your PDF resume once; the bot uses SBERT embeddings + Claude LLM to rank jobs by fit  
✅ **Multi-Board Scraping** — Aggregates jobs from Indeed, LinkedIn, Glassdoor, Naukri, RemoteOK, Adzuna, and more  
✅ **Telegram Delivery** — Get ranked job digests delivered to your Telegram bot with action buttons  
✅ **Assisted Auto-Apply** — Bot pre-fills Greenhouse/Lever/Ashby forms, sends a preview for your review, submits on confirmation  
✅ **Smart Deduplication** — Avoids showing the same job twice  
✅ **Scheduled Searches** — Runs on a schedule (default: every 6 hours) or on-demand  

## Tech Stack

- **Telegram Bot**: aiogram 3.x + APScheduler
- **Job Scraping**: python-jobspy (8+ boards) + free APIs
- **Resume Parsing**: pdfplumber (accurate PDF extraction)
- **Matching**: sentence-transformers (SBERT embeddings) + Claude LLM
- **Auto-Fill**: Playwright (async browser automation)
- **Database**: SQLite with aiosqlite

## Installation

### 1. Clone and Setup

```bash
cd job-search-bot
pip install -r requirements.txt
```

### 2. Install Playwright Browsers

```bash
python -m playwright install chromium
```

### 3. Configure Environment

Copy `.env.example` to `.env` and fill in your keys:

```bash
cp .env.example .env
```

**Required Keys:**
- `TELEGRAM_BOT_TOKEN` — Get from [@BotFather](https://t.me/botfather) on Telegram
- `ANTHROPIC_API_KEY` — Get from [Anthropic console](https://console.anthropic.com)

**Optional Keys (for richer job coverage):**
- `ADZUNA_APP_ID` & `ADZUNA_API_KEY` — Free registration at [Adzuna](https://developer.adzuna.com)

**Job Search Params:**
```env
SEARCH_KEYWORDS=Software Engineer
LOCATION=India
COUNTRY=india
SEARCH_INTERVAL_HOURS=6
```

## Running the Bot

```bash
python bot/main.py
```

The bot will:
1. Start polling for Telegram updates
2. Initialize the database
3. Schedule job searches to run every 6 hours

## Usage

### In Telegram

**1. Upload Resume**
```
/resume
[Attach your PDF resume]
```
Bot will parse it and compute a skill embedding.

**2. Trigger Search**
```
/search
```
Bot will immediately search all job boards and send you a ranked list.

**3. Review Jobs**
Each job appears as a message with buttons:
- ✅ **Apply** — Pre-fill the application form
- ⏭️ **Skip** — Mark as seen, move to next
- 💾 **Save** — Bookmark for later

**4. Assisted Apply**
When you tap "Apply":
1. Bot navigates to the job's application form
2. Pre-fills your name, email, phone, resume
3. Sends you a screenshot preview
4. Waits for your confirmation
5. Submits on your signal

**5. Check Status**
```
/status
```
Shows today's job count, applications sent.

```
/history
```
Lists all jobs you've applied to.

## Architecture

```
job-search-bot/
├── config.py                 # Load environment variables
├── bot/
│   ├── main.py               # Entry point; aiogram App + scheduler
│   ├── handlers.py           # Command handlers (/resume, /search, /status, etc.)
│   ├── scheduler.py          # APScheduler wrapper
│   └── keyboards.py          # Inline button layouts
├── matcher/
│   ├── resume_parser.py      # pdfplumber: PDF → structured JSON
│   ├── embedder.py           # SBERT: resume/job embeddings + ranking
│   └── llm_ranker.py         # Claude Haiku (bulk score) + Sonnet (cover letters)
├── scraper/
│   ├── jobspy_scraper.py     # JobSpy: Indeed, LinkedIn, Glassdoor, Naukri
│   ├── free_apis.py          # RemoteOK, Adzuna, Jobicy REST calls
│   └── aggregator.py         # Dedup jobs by URL + title+company
├── applier/
│   ├── ats_detector.py       # Detect ATS type from URL
│   ├── form_filler.py        # Playwright: per-ATS form filling
│   └── apply_session.py      # Manage apply state, screenshots, confirm/cancel
└── storage/
    └── db.py                 # SQLite: jobs, resume, pending applies
```

## How Matching Works

### Stage 1: Bulk Filtering (Free)
1. Parse resume with pdfplumber → extract text + skills
2. Compute SBERT embedding of resume (offline, free)
3. Score all new jobs via cosine similarity to resume embedding
4. Select top 50 candidates

### Stage 2: LLM Ranking (Cheap)
1. Pass top 50 to Claude Haiku (0.5¢)
2. Claude scores each 0–10 and gives a one-liner reason
3. Top 10–15 returned to user

### Stage 3: Cover Letter Generation (On Demand)
1. User taps "Apply" on a job
2. Claude Sonnet (5¢) generates a tailored cover letter
3. Bot pre-fills form + cover letter, sends preview

## Cost Estimates

| Component | Cost/Run |
|-----------|----------|
| Job search (all APIs) | $0 (free tier) |
| Resume embedding | $0 (local SBERT) |
| Haiku bulk scoring (50 jobs) | ~$0.005 |
| Sonnet cover letter (1 job) | ~$0.05 |
| **Monthly (~180 searches, 30 applies)** | ~**$2–3** |

## Limitations & Roadmap

### Current MVP
- ✅ Greenhouse / Lever / Ashby form filling
- ✅ LinkedIn job listings (no Easy Apply to avoid bans)
- ✅ Assisted apply only (human confirmation required)
- ✅ 6-hour schedule

### Known Limitations
- Workday forms are complex; partial fill only (v2 feature)
- Form filling is fragile if ATS updates DOM structure
- Some job postings may have custom fields bot can't fill

### Future Features (v2+)
- [ ] Fully autonomous apply with stricter success rate measurement
- [ ] Workday form automation
- [ ] Proxy rotation for high-volume scraping
- [ ] Resume versioning (tailor resume per job)
- [ ] Email summary digest
- [ ] Job board account login/apply via credentials
- [ ] Rich job card search UI (web dashboard)

## Troubleshooting

**Bot not responding to /start?**
- Check `TELEGRAM_BOT_TOKEN` in `.env` is correct
- Restart bot: `python bot/main.py`

**Resume parsing fails?**
- Ensure you're uploading a `.pdf` file
- Try a simpler PDF (some complex layouts confuse pdfplumber)
- Check `resumes/` folder for the uploaded file

**Jobs not found?**
- Check `SEARCH_KEYWORDS` and `LOCATION` in `.env`
- Verify internet connection
- Check if job board APIs are up: test with `/search` command

**Form filling fails?**
- Some ATS platforms change HTML structure frequently
- Try opening the job URL directly to see current form layout
- File an issue with the job board name + URL

**Claude API errors?**
- Verify `ANTHROPIC_API_KEY` in `.env` is valid
- Check you have API credits remaining
- Review [Claude pricing](https://www.anthropic.com/pricing)

## Contributing

Issues and PRs welcome! Key areas:
- ATS form filling (test more platforms)
- Job board API updates
- Resume parsing improvements
- Cover letter generation prompts

## License

MIT

## Contact

Have questions? Open an issue on GitHub or check the plan file at `.claude/plans/`.
