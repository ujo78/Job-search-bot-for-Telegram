# 🚀 Deployment Guide — Run Your Bot 24/7

Once you have your bot token and `.env` configured, you can deploy it. Here are all your options.

---

## Option 1: Local Testing (Your Computer)

### Best For: Testing before deployment

**Setup:**
```bash
cd "Desktop/job search bot"
python bot/main.py
```

**What happens:**
- Bot runs on your computer
- Stops when you close the terminal
- Perfect for testing `/resume`, `/search`, `/apply` flows

**Pros:**
- ✅ No setup needed
- ✅ Full control
- ✅ Easy debugging

**Cons:**
- ❌ Only works while your computer is on
- ❌ Not 24/7

---

## Option 2: Railway.app (Easiest Cloud Deployment)

### Best For: Free to $5/month, very easy

**Step 1: Sign Up**
1. Go to https://railway.app
2. Click "Start Project"
3. Sign in with GitHub (create GitHub account if needed)

**Step 2: Connect Your Code**
1. Click "Deploy from GitHub repo"
2. Authorize Railway to access GitHub
3. Select your job-search-bot repo (if you pushed to GitHub)
   - If not, use the alternative below

**Step 3 (Alternative): Upload Files Directly**
```bash
# If you haven't pushed to GitHub, Railway can deploy from folder
# Go to Railway, create new project
# Connect via CLI:
npm install -g railway
railway login
railway init
railway up
```

**Step 4: Set Environment Variables**
1. In Railway dashboard, go to your project
2. Click "Variables"
3. Add:
   - `TELEGRAM_BOT_TOKEN` = your token
   - `ANTHROPIC_API_KEY` = your key
   - `SEARCH_KEYWORDS` = "Software Engineer" (or your preference)
   - `LOCATION` = "India" (or your location)
   - `COUNTRY` = "india"

**Step 5: Deploy**
```bash
# In your project directory
git push
# or use Railway CLI
railway deploy
```

**Step 6: Check Status**
- Go to Railway dashboard
- Click "Deployments"
- See green ✅ if running

**Cost:** Free tier ~$5 free credits/month, then $5/month

**Logs:**
```bash
railway logs
```

---

## Option 3: Heroku (Simple, But Paid)

### Best For: $7/month, Procfile-based

**Step 1: Install Heroku CLI**
```bash
# Windows: download from https://devcenter.heroku.com/articles/heroku-cli
# Or use: choco install heroku-cli

heroku login
```

**Step 2: Create app.json**
In your project root, create `app.json`:
```json
{
  "name": "job-search-bot",
  "description": "Resume-driven job search automation via Telegram",
  "buildpacks": [
    {
      "url": "heroku/python"
    }
  ],
  "env": {
    "TELEGRAM_BOT_TOKEN": {
      "description": "Your Telegram bot token from @BotFather"
    },
    "ANTHROPIC_API_KEY": {
      "description": "Your Anthropic API key"
    }
  }
}
```

**Step 3: Create Procfile**
```bash
echo "worker: python bot/main.py" > Procfile
```

**Step 4: Deploy**
```bash
heroku create your-job-bot-name
heroku config:set TELEGRAM_BOT_TOKEN=your_token
heroku config:set ANTHROPIC_API_KEY=your_key
git push heroku main
```

**Step 5: Start Worker**
```bash
heroku ps:scale worker=1
heroku logs --tail
```

**Cost:** $7/month minimum (worker dyno)

---

## Option 4: DigitalOcean Droplet ($4-6/month)

### Best For: Full control, cheapest VPS

**Step 1: Create Droplet**
1. Go to https://digitalocean.com
2. Click "Create" → "Droplets"
3. Choose:
   - OS: Ubuntu 22.04
   - Size: $4/month (1GB RAM, 25GB SSD)
   - Region: Closest to you
4. Click "Create Droplet"

**Step 2: SSH Into Server**
```bash
# DigitalOcean sends you IP address
ssh root@your_droplet_ip
```

**Step 3: Install Dependencies**
```bash
apt update && apt upgrade -y
apt install python3-pip git -y
```

**Step 4: Clone Your Code**
```bash
git clone https://github.com/yourusername/job-search-bot.git
cd job-search-bot
pip install -r requirements.txt
python -m playwright install chromium
```

**Step 5: Create .env File**
```bash
cat > .env << EOF
TELEGRAM_BOT_TOKEN=your_token_here
ANTHROPIC_API_KEY=your_key_here
SEARCH_KEYWORDS=Software Engineer
LOCATION=India
COUNTRY=india
SEARCH_INTERVAL_HOURS=6
EOF
```

**Step 6: Run with nohup (Stays Running)**
```bash
nohup python bot/main.py > bot.log 2>&1 &
```

**Step 7: Verify it's running**
```bash
tail -f bot.log
```

Should see: `Bot started, polling for updates...`

**Step 8: Keep it running after SSH exit**
The `&` at the end keeps it running. Use:
```bash
ps aux | grep bot
```

to verify.

**Cost:** $4-6/month

**To stop:**
```bash
pkill -f "python bot/main.py"
```

---

## Option 5: AWS Lambda + Webhook (Serverless, Cheapest)

### Best For: Ultra-cheap, but more complex

Instead of polling, Lambda listens to Telegram webhook.

**Step 1: Create Lambda Function**
1. Go to AWS Lambda console
2. Create function: `job-bot`
3. Runtime: Python 3.11
4. Handler: `lambda_handler`

**Step 2: Update Code**
Replace the lambda function with webhook handler.

**Step 3: Set Environment Variables**
- TELEGRAM_BOT_TOKEN
- ANTHROPIC_API_KEY

**Step 4: Create API Gateway**
- Attach to Lambda
- Get HTTPS URL

**Step 5: Register Webhook**
```bash
curl -X POST "https://api.telegram.org/bot${YOUR_TOKEN}/setWebhook?url=${YOUR_LAMBDA_URL}"
```

**Cost:** Free tier (1M requests/month)

**Note:** More complex, requires refactoring bot code to use webhook instead of polling.

---

## Comparison Table

| Option | Cost | Setup Time | Reliability | Best For |
|--------|------|-----------|-------------|----------|
| Local | $0 | 5 min | Low | Testing |
| Railway | $0-5 | 10 min | High | Quick deploy |
| Heroku | $7 | 15 min | High | Simple |
| DigitalOcean | $4-6 | 20 min | Very High | Full control |
| AWS Lambda | Free | 30 min | High | Serverless |

---

## My Recommendation

For you (starting out):
1. **Test locally first** (5 min)
2. **Deploy to Railway** (10 min, free tier)
3. **Later: Move to DigitalOcean** if you want more control

This way you pay $0-5/month and the bot runs 24/7.

---

## Step-by-Step for Railway (Recommended)

### Prerequisites
- GitHub account
- Railway account (free signup)

### Complete Flow

**1. Push code to GitHub**
```bash
cd "Desktop/job search bot"
git init
git add .
git commit -m "Initial commit: Job search bot"
git branch -M main
git remote add origin https://github.com/yourusername/job-search-bot.git
git push -u origin main
```

**2. Go to Railway**
- https://railway.app
- Sign up with GitHub
- Create new project
- Select "Deploy from GitHub repo"
- Choose your job-search-bot repo

**3. Configure**
- Railway auto-detects Python
- Click "Add" → "Add Variable"
- Add variables:
  ```
  TELEGRAM_BOT_TOKEN = 123456:ABC...
  ANTHROPIC_API_KEY = sk-ant-...
  SEARCH_KEYWORDS = Software Engineer
  LOCATION = India
  COUNTRY = india
  ```

**4. Deploy**
- Railway automatically deploys when you push to GitHub
- Watch the "Deployments" tab
- See ✅ when running

**5. Check Logs**
- Click "Logs" to see bot output
- Should see "Bot started, polling for updates..."

**6. Test in Telegram**
- Message your bot
- Send `/start`
- Should work! 🎉

---

## Monitoring & Maintenance

### Check if Bot is Running

**Local:**
```bash
# Terminal where bot is running
# Should see updates in real-time
```

**Railway:**
```bash
# Dashboard → Logs
# Search for "polling" or "error"
```

**DigitalOcean:**
```bash
# SSH into droplet
ps aux | grep bot
tail -f bot.log
```

### Restart Bot

**Local:** `Ctrl+C`, then `python bot/main.py`

**Railway:** Push new code to GitHub → auto-redeploys

**DigitalOcean:**
```bash
ssh root@your_ip
pkill -f "python bot/main.py"
nohup python bot/main.py > bot.log 2>&1 &
```

### Update Code

**Local:** Edit files, restart

**Railway:**
```bash
git push  # Automatically redeploys
```

**DigitalOcean:**
```bash
ssh root@your_ip
cd job-search-bot
git pull
pkill -f "python bot/main.py"
nohup python bot/main.py > bot.log 2>&1 &
```

---

## Troubleshooting Deployment

**"Bot doesn't respond after deployment?"**
1. Check environment variables are set
2. Check logs for errors
3. Verify token is correct
4. Restart the bot/deployment

**"Database errors?"**
- SQLite works fine, but persists locally
- On restart, old data is preserved
- For multiple instances, upgrade to PostgreSQL (v2)

**"Form filling doesn't work?"**
- Playwright needs browser files
- Make sure `playwright install chromium` runs
- Check logs for browser errors

**"Out of memory?"**
- Free tier has 512MB
- Upgrade instance size
- Optimize embeddings caching

---

## Security Checklist

- [ ] Never commit `.env` to GitHub
- [ ] `.gitignore` has `.env` entry
- [ ] Token is in environment variables, not code
- [ ] ANTHROPIC_API_KEY is secret
- [ ] Logs don't print sensitive data
- [ ] Server uses HTTPS (Railway/Heroku do this)

---

## Next Steps

1. Choose deployment method (Railway recommended)
2. Follow setup steps above
3. Test in Telegram
4. Monitor logs
5. Update search settings as needed

**You're ready to deploy!** 🚀
