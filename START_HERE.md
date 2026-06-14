# 🚀 Getting Started Now

## The Bot is Ready. Here's How to Run It.

### 1. Get Your API Keys (5 minutes)

**Telegram Bot Token:**
1. Open Telegram → search for @BotFather
2. Send `/start` → `/newbot`
3. Name your bot (e.g., "JobSearchBot")
4. You'll get a token like: `123456789:ABCdefGHIjklmnoPQRstuvWXYZabcd`

**Anthropic API Key:**
1. Go to https://console.anthropic.com/account/keys
2. Create a new API key
3. Copy it (looks like `sk-ant-...`)

### 2. Configure the Bot (2 minutes)

```bash
cd "Desktop/job search bot"

# Copy template
cp .env.example .env

# Open .env in any text editor and fill in:
TELEGRAM_BOT_TOKEN=your_token_here
ANTHROPIC_API_KEY=your_key_here
```

Optional customization:
```env
SEARCH_KEYWORDS=Python Developer      # What jobs to search for
LOCATION=San Francisco                # Where to search
COUNTRY=usa                           # usa, india, canada, uk, etc
SEARCH_INTERVAL_HOURS=6               # How often to auto-search
```

### 3. Start the Bot (1 minute)

```bash
python bot/main.py
```

You should see:
```
INFO:root:Bot started, polling for updates...
```

Leave this running (don't close the terminal).

### 4. Test in Telegram (5 minutes)

1. **Open Telegram** and find your bot
2. Send: `/start`
   - You'll see welcome message with command list
3. Send: `/resume`
   - Bot says "Upload PDF"
4. **Attach any PDF** (your actual resume, or test PDF)
   - Bot extracts skills and experiences
5. Send: `/search`
   - Bot scrapes all job sources (30-60 seconds)
   - Shows top 10 matching jobs
   - First job appears with 3 buttons
6. **Tap "Apply"** on any job
   - Bot fills out the form preview
   - Sends screenshot
7. **Tap "Confirm & Submit"**
   - Form submits automatically
   - Confirmation message

Done! 🎉

### What Happens Next

- Searches will run **automatically every 6 hours** (configurable)
- Jobs are stored in `job_search.db` (SQLite)
- Screenshots saved to `screenshots/` folder
- Resume stored in `resumes/` folder

### Troubleshooting

**"Bot doesn't respond?"**
- Make sure `python bot/main.py` is still running
- Check TELEGRAM_BOT_TOKEN is correct

**"No jobs found?"**
- Try different SEARCH_KEYWORDS (e.g., "engineer" not "Senior ML Engineer")
- Check internet connection
- Give it 60 seconds (scraping takes time)

**"Form submission fails?"**
- Some job sites have complex dynamic forms
- You'll get a "verify at URL" message with the job link
- Open manually and apply

**"Form preview doesn't show?"**
- Some ATS platforms aren't supported yet (v2 feature)
- You can still view the job and apply manually

### Commands in Telegram

| Command | What it does |
|---------|-------------|
| `/start` | Initialize bot |
| `/resume` | Upload/update resume |
| `/search` | Find matching jobs (manual trigger) |
| `/status` | See today's stats |
| `/history` | View all applied jobs |

### File Structure (If You Care)

```
job-search-bot/
├── bot/main.py              ← Start here
├── bot/handlers.py          ← Telegram commands
├── matcher/embedder.py      ← Resume matching
├── scraper/jobspy_scraper.py ← Job scraping
├── applier/form_filler.py   ← Auto-apply
└── storage/db.py            ← Database
```

### Costs

**Free tier:** JobSpy + RemoteOK + free APIs = **$0**
**With Claude:** ~$0.005/search + $0.05/apply = **~$2/month**

### Support

- See `README.md` for full documentation
- See `IMPLEMENTATION_COMPLETE.md` for technical details
- See `IMPLEMENTATION_ROADMAP.md` for what's next

---

**You're all set!** Run `python bot/main.py` and test it out. 🚀
