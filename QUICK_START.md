# Quick Start Guide - WorkHub Telegram Bot

## 🚀 Fast Setup (5 Minutes)

### 1. Prerequisites Checklist
- [ ] Python 3.8+ installed
- [ ] Telegram account
- [ ] Supabase account (free tier works)

### 2. Create Telegram Bot (2 minutes)
1. Open Telegram, search for `@BotFather`
2. Send `/newbot` command
3. Follow prompts to name your bot
4. **Copy the bot token** (looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 3. Create Telegram Channel (1 minute)
1. Create a new public Telegram channel
2. Add your bot as an administrator
3. Note the channel username (e.g., `@myworkhubchannel`)

### 4. Get Your Telegram User ID (30 seconds)
1. Message `@userinfobot` on Telegram
2. Copy your User ID number

### 5. Setup Supabase (2 minutes)
1. Go to [supabase.com](https://supabase.com) and create account
2. Create a new project
3. Go to **SQL Editor** and run the contents of `supabase_schema.sql`
4. Go to **Storage** → Create two buckets:
   - `task-documents` (set to Public)
   - `task-videos` (set to Public)
5. Go to **Settings** → **API** and copy:
   - Project URL
   - anon/public key

### 6. Install and Configure (1 minute)

```bash
# Clone/Download this repository
cd telegram-workhub-bot

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
```

Edit `.env` with your values:
```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=your_supabase_anon_key
TELEGRAM_CHANNEL_ID=@yourchannel
TELEGRAM_CHANNEL_NAME=Your Channel Name
ADMIN_TELEGRAM_UID=your_user_id
```

### 7. Run the Bot

```bash
python bot.py
```

You should see:
```
INFO - Bot started successfully!
```

### 8. Test the Bot

1. Open Telegram and search for your bot
2. Send `/start` command
3. Click "Join Channel" → "Verify Join"
4. You should see the main menu!

## 🎉 You're Done!

Your WorkHub bot is now running! Here's what to do next:

### As Admin:
1. Send `/start` to your bot
2. You'll see the Admin Dashboard (since you set ADMIN_TELEGRAM_UID)
3. Go to **Manage Payment Info** and update:
   - UPI ID for deposits
   - Crypto wallet address (if accepting crypto)

### As Provider:
1. Use a different Telegram account
2. Send `/start` and verify channel join
3. Click "Register as Provider"
4. Complete registration
5. Add balance and create your first task!

### As Worker:
1. Use another Telegram account
2. Send `/start` and verify channel join
3. Click "Complete Registration"
4. Browse tasks and start earning!

## 📱 Features Overview

### Provider Dashboard
- ➕ Create New Task
- 📋 View My Tasks
- 💰 Wallet (Add/Withdraw)
- 🎁 Refer & Earn
- 📢 Run Campaign (track performance)
- 📊 Lifetime Earn (analytics)
- 💬 Support

### Worker Dashboard
- 🎯 Get New Task (by category)
- 📝 My Tasks
- 💰 Wallet (Add/Withdraw)
- 🎁 Refer & Earn
- 💬 Support

### Admin Dashboard
- 👥 View All Users
- 📋 View All Tasks
- ✅ Approve Transactions
- 💬 Support Messages
- ⚙️ Manage Payment Info
- 📂 Manage Categories
- 📊 View Referrals
- ✔️ Approve Task Proofs

## 🔧 Configuration Options

Edit `config.py` to customize:

```python
MIN_DEPOSIT = 1              # Minimum deposit amount (₹)
MAX_DEPOSIT = 10000          # Maximum deposit amount (₹)
MIN_WITHDRAWAL = 150         # Minimum withdrawal amount (₹)
MAX_DOCUMENT_SIZE = 300 * 1024    # 300 KB
MAX_VIDEO_SIZE = 10 * 1024 * 1024 # 10 MB
REFERRAL_BONUS = 50          # Referral bonus (₹)
PAYMENT_VERIFICATION_DELAY = 120  # Wait time before UTR submission (seconds)
```

## 🆘 Troubleshooting

**Bot doesn't respond**
- Check if `bot.py` is still running
- Verify bot token in `.env`
- Check internet connection

**Channel verification fails**
- Make sure bot is added as admin in channel
- Use channel username with @ (e.g., `@channel`)
- Ensure you've actually joined the channel

**Database errors**
- Verify Supabase URL and key in `.env`
- Make sure you ran `supabase_schema.sql` in SQL Editor
- Check Supabase dashboard for error logs

**File upload fails**
- Verify Supabase storage buckets exist:
  - `task-documents`
  - `task-videos`
- Make sure buckets are set to Public
- Check file size limits

## 💡 Pro Tips

1. **Test with Multiple Accounts**: Use different Telegram accounts to test as Provider, Worker, and Admin
2. **Monitor Logs**: Keep an eye on the terminal for error messages
3. **Backup Database**: Regularly export your Supabase database
4. **Update Payment Info**: Keep UPI and Crypto addresses current
5. **Respond to Support**: Check support messages regularly

## 📚 Need More Help?

- Read the full [README.md](README.md) for detailed documentation
- Check [SETUP_SUMMARY.md](SETUP_SUMMARY.md) for comprehensive setup guide
- Review [FAQ.md](FAQ.md) for common questions
- See [TESTING.md](TESTING.md) for testing procedures

## 🚀 Going to Production

For production deployment:

1. **Use a VPS/Cloud Server** (AWS, DigitalOcean, Heroku, Railway, etc.)
2. **Keep bot running 24/7** (use systemd, PM2, or supervisor)
3. **Enable HTTPS** for webhooks (optional, polling works fine)
4. **Monitor performance** (set up logging and alerts)
5. **Regular backups** (database and configuration)
6. **Security**: Never commit `.env` to git

Example systemd service (`/etc/systemd/system/workhub-bot.service`):

```ini
[Unit]
Description=WorkHub Telegram Bot
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/telegram-workhub-bot
Environment="PATH=/path/to/telegram-workhub-bot/venv/bin"
ExecStart=/path/to/telegram-workhub-bot/venv/bin/python bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable workhub-bot
sudo systemctl start workhub-bot
sudo systemctl status workhub-bot
```

---

**Happy Bot Building! 🎉**

Need help? Open an issue or contact support through the bot's support feature.
