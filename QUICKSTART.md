# Quick Start Guide

Get WorkHub Bot running in 10 minutes!

## Prerequisites Checklist

- [ ] Python 3.8+ installed
- [ ] Telegram account
- [ ] Supabase account (free tier is fine)
- [ ] 10 minutes of your time

## Step-by-Step Setup

### 1. Get Your Bot Token (2 minutes)

1. Open Telegram
2. Search for `@BotFather`
3. Send `/newbot`
4. Follow prompts:
   - Bot name: `WorkHub Bot`
   - Username: `your_workhub_bot` (must end with 'bot')
5. Copy the token (looks like: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 2. Create Your Channel (1 minute)

1. In Telegram, create a new channel
2. Name it (e.g., "WorkHub Community")
3. Add your bot as admin:
   - Channel settings → Administrators → Add Administrator
   - Search for your bot
   - Grant admin rights
4. Note the channel username (e.g., `@workhub_community`)

### 3. Setup Supabase (3 minutes)

1. Go to [supabase.com](https://supabase.com)
2. Sign up/Login
3. Create new project:
   - Name: `workhub-bot`
   - Database password: (save this!)
   - Region: Choose closest to you
   - Wait 2 minutes for project creation

4. Once created, go to **SQL Editor**
5. Click "New Query"
6. Copy entire content from `supabase_schema.sql`
7. Paste and click "Run"
8. Wait for "Success" message

9. Get your credentials:
   - Settings → API
   - Copy `Project URL`
   - Copy `anon` `public` key

10. Create storage buckets:
    - Storage → Create bucket → `task-documents` (Public)
    - Storage → Create bucket → `task-videos` (Public)

### 4. Get Your Telegram User ID (1 minute)

1. In Telegram, search for `@userinfobot`
2. Send `/start`
3. Copy your ID (number like `123456789`)

### 5. Install Bot (2 minutes)

```bash
# Download/Clone project
cd telegram-workhub-bot

# Run setup script (Linux/Mac)
./setup.sh

# Or manually:
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 6. Configure Environment (1 minute)

1. Copy example environment file:
```bash
cp .env.example .env
```

2. Edit `.env`:
```bash
nano .env  # or use any text editor
```

3. Fill in your details:
```env
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=your_supabase_anon_key_here
TELEGRAM_CHANNEL_ID=@workhub_community
TELEGRAM_CHANNEL_NAME=WorkHub Community
ADMIN_TELEGRAM_UID=123456789
```

4. Save and close (Ctrl+X, Y, Enter for nano)

### 7. Run the Bot! (30 seconds)

```bash
# Activate virtual environment if not active
source venv/bin/activate  # Windows: venv\Scripts\activate

# Start the bot
python bot.py
```

You should see:
```
INFO - Bot started successfully!
```

### 8. Test Your Bot (1 minute)

1. Open Telegram
2. Search for your bot
3. Send `/start`
4. Join the channel when prompted
5. Verify membership
6. Explore the features!

## Troubleshooting Quick Fixes

### "No module named 'telegram'"
```bash
pip install -r requirements.txt
```

### "Connection error"
- Check internet connection
- Verify bot token is correct
- Check Supabase URL and key

### "Channel verification fails"
- Ensure bot is channel admin
- Check channel ID starts with @
- Try leaving and rejoining channel

### Bot doesn't respond
- Check bot.py is running
- Restart bot: Ctrl+C then `python bot.py`
- Check Telegram API status

## What's Next?

### Configure Payment Methods (Admin)

1. Start bot as admin
2. Admin Dashboard → Manage Payment Info
3. Update UPI ID for deposits
4. Update Crypto wallet address

### Create Your First Task (Provider)

1. Register as Provider
2. Add balance to wallet
3. Create New Task
4. Wait for workers to apply

### Complete Your First Task (Worker)

1. Get New Task
2. Browse available tasks
3. Accept a task
4. Complete and submit proof
5. Get paid!

## Next Steps

- Read [README.md](README.md) for detailed documentation
- Check [FAQ.md](FAQ.md) for common questions
- Review [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment
- See [CONTRIBUTING.md](CONTRIBUTING.md) to contribute

## Production Deployment

For production use:

1. **VPS Deployment** (Recommended):
```bash
# On your VPS
git clone your-repo
cd telegram-workhub-bot
./setup.sh
# Edit .env with production credentials
sudo nano /etc/systemd/system/workhub-bot.service
# (See DEPLOYMENT.md for systemd configuration)
sudo systemctl enable workhub-bot
sudo systemctl start workhub-bot
```

2. **Heroku Deployment**:
```bash
heroku create your-app-name
git push heroku main
heroku config:set TELEGRAM_BOT_TOKEN=...
# (Set all env vars)
heroku ps:scale worker=1
```

3. **Docker Deployment**:
```bash
docker build -t workhub-bot .
docker run -d --env-file .env workhub-bot
```

## Support

Need help?
- Check [FAQ.md](FAQ.md)
- Review [README.md](README.md)
- Contact support through bot
- Open an issue on GitHub

## Congratulations! 🎉

Your WorkHub Bot is now running! Share it with your community and start connecting work providers with workers.

---

**Remember**: This bot handles real money. Always:
- Keep backups of your database
- Monitor transactions regularly
- Verify all payments manually
- Have clear terms & conditions
- Test thoroughly before production use

**Happy Bot Running! 🚀**
