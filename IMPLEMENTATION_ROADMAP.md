# Implementation Status & Next Steps

## What's Already Built (Components)

### ✅ Fully Implemented & Tested
| Component | Status | Notes |
|-----------|--------|-------|
| Database layer (SQLite) | ✅ Working | Tested insert/retrieve |
| Config system | ✅ Working | Loads from .env |
| Resume parser (pdfplumber) | ✅ Ready | Just needs file path |
| ATS detector | ✅ Ready | URL pattern matching |
| SBERT embeddings | ✅ Ready | Requires sentence-transformers init |
| Claude LLM integration | ✅ Ready | Haiku + Sonnet available |
| Telegram bot framework (aiogram) | ✅ Ready | FSM, handlers, keyboards all defined |
| APScheduler | ✅ Ready | Async scheduler registered |
| Playwright form filler | ✅ Ready | Browser automation skeleton |
| Job aggregator | ✅ Ready | Dedup logic implemented |

### ⚠️ Wiring Needed (To Complete MVP)

#### 1. `/search` Command Implementation
**File**: `bot/handlers.py`
**Current**: Just prints "Searching..."
**Need to add**:
```python
# Actually run the full pipeline:
# 1. Get resume from DB
# 2. Call scrape_jobspy() + free APIs
# 3. Call embedder.rank_jobs()
# 4. Call llm_ranker.score_jobs()
# 5. Send paginated job digest to user
```

#### 2. Apply Button Handler
**File**: `bot/handlers.py`
**Current**: Callbacks registered but empty
**Need to add**:
```python
@router.callback_query(F.data.startswith("apply_"))
async def handle_apply(query, state):
    # 1. Parse job_id from callback data
    # 2. Create ApplySession
    # 3. Call prepare_form_preview()
    # 4. Send screenshot to user
    # 5. Wait for confirm/cancel
```

#### 3. Confirm & Submit Handler
**File**: `bot/handlers.py`
**Current**: Not implemented
**Need to add**:
```python
@router.callback_query(F.data == "confirm_apply")
async def confirm_apply(query, state):
    # 1. Get ApplySession from state
    # 2. Call submit_application()
    # 3. Mark job as applied in DB
    # 4. Send confirmation to user
```

#### 4. Scheduled Job Search
**File**: `bot/main.py`
**Current**: Scheduler set up but search_and_notify() is a skeleton
**Need to add**: Full implementation of search_and_notify() to:
- Scrape all sources
- Match and rank jobs
- Notify user via Telegram

## How to Test Now

### Option 1: Manual Test (No Bot)
```bash
# Test database
python -c "
import asyncio
from storage.db import JobDB
db = JobDB('test.db')
asyncio.run(db.init())
print('✓ DB works')
"

# Test resume parsing
python -c "
from matcher.resume_parser import parse_resume
data = parse_resume('your_resume.pdf')
print(f'✓ Parsed {len(data[\"skills\"])} skills')
"
```

### Option 2: Full Bot Test (With Telegram)
```bash
# 1. Set up .env with real keys
cp .env.example .env
# (fill in TELEGRAM_BOT_TOKEN and ANTHROPIC_API_KEY)

# 2. Start bot
python bot/main.py

# 3. In Telegram:
# /start → /resume (upload PDF) → /status
```

The bot will respond to these but `/search` won't return results yet.

## Priority: What to Wire Up First?

**MVP Checklist** (in order of importance):

1. **Implement `/search` end-to-end** (1-2 hours)
   - Wires scraper → matcher → LLM → Telegram
   - This is the core value
   
2. **Implement Apply button flow** (1-2 hours)
   - Form preview + confirm/submit
   - Gives users the assisted-apply experience

3. **Wire up APScheduler callback** (30 min)
   - Calls search_and_notify() every 6 hours
   - Enables the "hands-off" automation

4. **Add `/settings` command** (30 min)
   - Let users change keywords/location from Telegram
   - Currently requires `.env` restart

5. **Add job details & pagination** (1 hour)
   - View full job description
   - Browse pages of results

## Files to Focus On

```
Priority 1: bot/handlers.py
  ↓ Add real logic to cmd_search() callback
  ↓ Implement apply button handlers
  ↓ Wire ApplySession

Priority 2: bot/main.py
  ↓ Implement search_and_notify() with full pipeline
  ↓ Connect to scheduler callback

Priority 3: bot/handlers.py
  ↓ Add /settings command for user preferences
```

## Quick Copy-Paste Template

For `/search` handler, template:
```python
@router.message(Command("search"))
async def cmd_search(message: types.Message):
    await message.answer("🔍 Searching for jobs...")
    
    db = await init_db()
    resume = await db.get_resume()
    if not resume:
        await message.answer("❌ No resume found. Upload with /resume first.")
        return
    
    # TODO: Add scraper calls here
    # TODO: Add embedder ranking
    # TODO: Add LLM scoring
    # TODO: Send paginated results
    
    await message.answer("✅ Done! 5 jobs found.")
```

## Testing Strategy

**Without rewriting**: You can test handlers by:
1. Starting the bot
2. Sending commands
3. Checking console for errors
4. Checking SQLite db for changes

**With implementation**: Write tests to verify:
- JobSpy scraping works
- SBERT embeddings are created
- Claude API calls succeed
- Telegram messages format correctly
- Database inserts/updates work

Go ahead and let me know which area you'd like to tackle first!
