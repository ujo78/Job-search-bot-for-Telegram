# 🤖 Telegram Bot Setup Guide — Step by Step

## Step 1: Get Your Bot Token from BotFather

### What is BotFather?
BotFather is Telegram's official bot for creating and managing bots. It's like a bot factory.

### How to Create Your Bot

**1. Open Telegram** (mobile app or web at web.telegram.org)

**2. Search for @BotFather**
   - Click the search icon (magnifying glass)
   - Type: `@BotFather`
   - Click the bot with the purple robot icon

**3. Start the Bot**
   - Click "START" button
   - You'll see a menu with options

**4. Create a New Bot**
   - Send command: `/newbot`
   - Or click the "Create a new bot" button

**5. Name Your Bot**
   - BotFather asks: "What should your bot be called?"
   - Reply: `JobSearchBot` (or any name you like)
   - This is the display name users see

**6. Set Bot Username**
   - BotFather asks: "Give your bot a username"
   - Reply: `job_search_bot_yourname` 
   - **⚠️ IMPORTANT: Username must:**
     - End with `_bot` or `Bot`
     - Be unique (no one else can have it)
     - Only contain letters, numbers, underscores
   - Example: `job_search_bot_2024` or `my_job_bot`

**7. Get Your Token**
   - BotFather sends you a message like:
   ```
   ✅ Done! Congratulations on your new bot. 
   You will find it at t.me/your_bot_username. 
   You can now add a description, about section and profile picture for your bot, 
   see /help for a list of commands.
   
   Use this token to access the HTTP API:
   123456789:ABCdefGHIjklmnoPQRstuvWXYZabcd_example
   
   Keep your token secure and store it safely!
   ```

**8. Copy Your Token**
   - Long press on the token (the long string starting with numbers)
   - Click "Copy"
   - Save it somewhere safe temporarily

---

## Step 2: Add Token to .env File

You already have `.env.example` open. Now:

**1. In that file, find this line:**
```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
```

**2. Replace `your_telegram_bot_token_here` with your actual token**

For example:
```env
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklmnoPQRstuvWXYZabcd_example
```

**3. While you're there, also add Anthropic key:**
```env
ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
```

(Get Anthropic key from https://console.anthropic.com/account/keys)

**4. Save the file** (Ctrl+S)

---

## Step 3: Deploy the Bot Locally

### For Testing (Run on Your Computer)

**1. Open Terminal/Command Prompt**
```bash
cd "Desktop/job search bot"
```

**2. Start the bot**
```bash
python bot/main.py
```

You should see:
```
INFO:root:Bot started, polling for updates...
```

**✅ Leave this running!** Don't close the terminal.

**3. Test in Telegram**

Go to Telegram and:
- Search for your bot (by the username you chose, e.g., `@job_search_bot_2024`)
- Click on it
- Tap **START** button
- You should see the welcome message!

Try commands:
```
/start          ← See welcome
/resume         ← Upload a PDF
/search         ← Find jobs
/status         ← Check stats
/history        ← See applied jobs
```

---

## Step 4: Deploy the Bot on a Server (24/7)

For the bot to run 24/7 without your computer on, deploy it to a server.

### Free/Cheap Options

#### Option A: Heroku (Easiest, Free Tier Limited)
```bash
# Install Heroku CLI
# Create Procfile:
echo "worker: python bot/main.py" > Procfile

# Deploy
heroku create your-job-bot
heroku config:set TELEGRAM_BOT_TOKEN=your_token
heroku config:set ANTHROPIC_API_KEY=your_key
git push heroku main
heroku logs --tail
```

#### Option B: Railway.app (Free Tier, $5 after)
1. Go to https://railway.app
2. Sign up with GitHub
3. Create new project → Deploy from GitHub
4. Connect your repo
5. Add environment variables (TELEGRAM_BOT_TOKEN, ANTHROPIC_API_KEY)
6. Deploy

#### Option C: DigitalOcean Droplet ($4-6/month)
```bash
# Create Ubuntu droplet
# SSH in and run:
git clone your-repo
cd job-search-bot
pip install -r requirements.txt
nohup python bot/main.py > bot.log 2>&1 &
```

#### Option D: AWS EC2 Free Tier (12 months free)
- Similar to DigitalOcean
- More complex but free first year

#### Option E: Google Cloud Run (Free tier ~$0-3/month)
```bash
gcloud deploy push --image gcr.io/your-project/job-bot .
```

---

## Quick Checklist

- [ ] Opened @BotFather in Telegram
- [ ] Created bot with `/newbot`
- [ ] Copied the token
- [ ] Pasted token in `.env` file (TELEGRAM_BOT_TOKEN=...)
- [ ] Got Anthropic API key
- [ ] Pasted key in `.env` file (ANTHROPIC_API_KEY=...)
- [ ] Saved `.env` file
- [ ] Opened terminal in bot directory
- [ ] Ran `python bot/main.py`
- [ ] Searched for bot in Telegram
- [ ] Tapped START
- [ ] Saw welcome message ✅

---

## Troubleshooting

### "Bot doesn't respond in Telegram?"

**Check 1: Is bot running?**
- Look at your terminal
- Should say "Bot started, polling for updates..."
- If not, run: `python bot/main.py`

**Check 2: Wrong token?**
- Go back to @BotFather
- Send `/mybots`
- Click your bot
- Click "API Token"
- Copy again and paste in `.env`
- Save `.env`
- Restart bot: `Ctrl+C` then `python bot/main.py`

**Check 3: Token has space or extra character?**
- Token must be exact
- No spaces before or after
- Should be one long string

**Check 4: .env file not saved?**
- Make sure `.env` is saved (Ctrl+S)
- Don't edit `.env.example`, edit `.env`

### "Can't find bot in Telegram?"

- Use the **exact username** BotFather gave you
- Add `@` before it (e.g., `@job_search_bot_2024`)
- Make sure you spelled it right
- If still stuck, go to @BotFather, `/mybots`, click your bot, it shows the URL

### "Token is expired/invalid?"

- Go to @BotFather
- `/mybots` → your bot → "API Token"
- Copy the new token
- Update `.env`
- Restart bot

---

## What Happens Next

Once bot is running:

1. **User uploads resume**
   ```
   /resume
   [Upload PDF]
   ✅ Parsed: 15 skills, 3 experience entries
   ```

2. **Bot searches jobs**
   ```
   /search
   🔍 Searching...
   ✅ Found 32 jobs, showing top 10
   [Job card with Apply/Skip/Save buttons]
   ```

3. **User applies to job**
   ```
   [Tap Apply]
   ⏳ Preparing form...
   [Screenshot of pre-filled form]
   [Tap Confirm & Submit]
   ✅ Application submitted!
   ```

4. **Bot runs automatically**
   Every 6 hours (configurable), bot searches and sends new jobs

---

## Security Tips

⚠️ **Protect your tokens!**

- ✅ Keep `.env` file safe (added to `.gitignore`)
- ✅ Never share your token publicly
- ✅ Never commit `.env` to GitHub
- ❌ Don't post screenshots with token visible
- ❌ Don't share token in chat

If you accidentally share token:
- Go to @BotFather
- `/mybots` → your bot → "API Token"
- Revoke old token (makes it invalid)
- Generate new token

---

## Next Steps

1. ✅ Get token from @BotFather
2. ✅ Add to `.env`
3. ✅ Run bot locally: `python bot/main.py`
4. ✅ Test in Telegram
5. ✅ (Optional) Deploy to server for 24/7

You're ready! Let me know if you hit any issues. 🚀
