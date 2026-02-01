# WorkHub Telegram Bot

A comprehensive Telegram bot that connects work providers and work takers. The bot features three dashboards (Provider, Worker/Taker, and Admin) with complete wallet management, task assignment, and referral systems.

## Features

### 🌟 Core Features
- **Channel Verification**: Users must join a Telegram channel before accessing features
- **Three User Roles**: Provider, Worker/Taker, and Admin with distinct dashboards
- **Wallet System**: Add balance via UPI/Crypto, withdraw funds with admin verification
- **Task Management**: Create, assign, submit, and approve tasks
- **Referral System**: Earn bonuses for referring new users
- **File Uploads**: Support for documents (300KB max) and videos (10MB max)
- **Admin Dashboard**: Comprehensive management tools

### 👔 Provider Dashboard
- Register with complete profile (name, email, mobile, gender, DOB, location, password)
- Create tasks with categories, rewards, and slots (automatically deducted from wallet)
- View and manage tasks
- Run Campaign: Track active campaigns with performance metrics
- Lifetime Earn: View comprehensive financial and activity statistics
- Wallet with deposit/withdrawal (UPI/Crypto)
- Refer & Earn (₹50 per referral)
- Support system
- Receive notifications when workers submit task proofs

### 🎯 Work Taker Dashboard
- Complete registration form (name, mobile, DOB, password, referral code)
- Browse and accept tasks by category
- Submit task completion proof (documents up to 300KB, videos up to 10MB)
- Files stored securely in Supabase Storage
- Wallet management with deposit/withdrawal
- Refer & Earn (₹50 per referral)
- Support system
- Receive notifications when tasks are approved/rejected
- Auto-payment to wallet upon task approval

### 🔧 Admin Dashboard
- View all users, tasks, and assignments
- Approve/reject wallet transactions
- Review and approve task submissions
- Manage payment information (UPI/Crypto)
- Manage task categories
- View all referrals
- Handle support messages

## Tech Stack

- **Python 3.8+**
- **python-telegram-bot 20.7**: Telegram Bot API wrapper
- **Supabase**: PostgreSQL database and file storage
- **QRCode**: Generate payment QR codes
- **Validators**: Email and phone validation

## Setup Instructions

### 1. Prerequisites

- Python 3.8 or higher
- Supabase account
- Telegram Bot Token (from [@BotFather](https://t.me/botfather))
- Telegram Channel for verification

### 2. Create Telegram Bot

1. Open Telegram and search for [@BotFather](https://t.me/botfather)
2. Send `/newbot` command
3. Follow instructions to create your bot
4. Copy the bot token

### 3. Create Telegram Channel

1. Create a new Telegram channel
2. Add your bot as an administrator
3. Note the channel username (e.g., @yourchannel)

### 4. Setup Supabase

1. Go to [Supabase](https://supabase.com) and create a new project
2. Once created, go to **SQL Editor**
3. Copy the contents of `supabase_schema.sql` and execute it
4. Go to **Settings** → **API** and copy:
   - Project URL (SUPABASE_URL)
   - Anon/Public key (SUPABASE_KEY)
5. Go to **Storage** and create two buckets:
   - `task-documents`
   - `task-videos`
   - Set both to **Public** or configure appropriate policies

### 5. Install Dependencies

```bash
# Clone the repository or navigate to the project directory
cd telegram-workhub-bot

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 6. Configure Environment Variables

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and fill in your credentials:
   ```env
   TELEGRAM_BOT_TOKEN=your_bot_token_from_botfather
   SUPABASE_URL=https://xxxxx.supabase.co
   SUPABASE_KEY=your_supabase_anon_key
   TELEGRAM_CHANNEL_ID=@yourchannel
   TELEGRAM_CHANNEL_NAME=Your Channel Name
   ADMIN_TELEGRAM_UID=your_telegram_user_id
   ```

### 7. Get Your Telegram User ID

To set yourself as admin, you need your Telegram User ID:

1. Send a message to [@userinfobot](https://t.me/userinfobot)
2. Copy your User ID
3. Update `ADMIN_TELEGRAM_UID` in `.env`

### 8. Run the Bot

```bash
python bot.py
```

You should see:
```
INFO - Bot started successfully!
```

### 9. Test the Bot

1. Open Telegram and search for your bot
2. Send `/start` command
3. Follow the channel verification process
4. Explore the features!

## Database Schema

The bot uses the following Supabase tables:

- **users**: User profiles and wallet balances
- **categories**: Task categories
- **tasks**: Work provider tasks
- **task_assignments**: Task assignments to workers
- **wallet_transactions**: All wallet transactions
- **referrals**: Referral tracking
- **support_messages**: User support requests
- **payment_info**: Admin-managed payment methods

## Configuration

Edit `config.py` to customize:

```python
MIN_DEPOSIT = 1              # Minimum deposit amount
MAX_DEPOSIT = 10000          # Maximum deposit amount
MIN_WITHDRAWAL = 150         # Minimum withdrawal amount
MAX_DOCUMENT_SIZE = 300 * 1024  # 300 KB
MAX_VIDEO_SIZE = 10 * 1024 * 1024  # 10 MB
REFERRAL_BONUS = 50          # Referral bonus amount
PAYMENT_VERIFICATION_DELAY = 120  # 2 minutes wait for payment
```

## Usage Guide

### For Work Providers

1. **Register**: `/start` → Register as Work Provider
   - Complete registration form with all details
   - Enter referral code if you have one (optional)
2. **Create Task**: Dashboard → Create New Task
   - Enter task details (title, description, requirements)
   - Select category
   - Set reward amount per worker
   - Specify number of workers needed
   - Ensure sufficient wallet balance (cost = reward × workers)
   - Task cost is automatically deducted from wallet
3. **Manage Tasks**: View My Tasks to see all your tasks and their status
4. **Run Campaign**: Track all active campaigns with:
   - Total slots and filled slots
   - Total budget allocated
   - Completion rates for each campaign
5. **Lifetime Earn**: View comprehensive analytics:
   - Total deposits, withdrawals, and spending
   - Referral earnings
   - Total tasks created and workers hired
   - ROI metrics (average task cost, cost per worker)
6. **Add Balance**: Wallet → Add Balance
   - Enter amount (₹1 - ₹10,000)
   - Choose UPI or Crypto
   - Get QR code / wallet address
   - Wait 2 minutes, then submit UTR/Transaction ID
   - Admin will verify and approve
7. **Withdraw**: Wallet → Withdraw
   - Minimum: ₹150
   - Choose method (UPI/Bank/Crypto)
   - Enter payment details and amount
   - Admin will process within 2-5 business days
8. **Refer & Earn**: Share your referral code
   - Earn ₹50 for each new user who signs up
   - Track all your referrals and earnings
9. **Notifications**: Receive Telegram messages when:
   - Workers submit task completion proofs

### For Work Takers

1. **Register**: `/start` → Complete Registration
   - Enter full name, mobile number, date of birth
   - Create password for your account
   - Enter referral code if you have one (optional)
2. **Find Tasks**: Get New Task
   - Browse all tasks or filter by category
   - View task details, rewards, and available slots
3. **Take Task**: Click on any available task
   - Review requirements carefully
   - Accept task to add to "My Tasks"
4. **Submit Proof**: My Tasks → Submit Task
   - Upload document (PDF, DOCX, PPT, PNG, JPG - max 300KB)
   - Upload video (MP4, AVI, MKV - max 10MB)
   - At least one file (document or video) is required
   - Files are securely stored in Supabase Storage
5. **Get Paid**: Automatic payment after admin approval
   - Receive notification when task is approved
   - Payment added to wallet instantly
   - Check transaction history in Wallet
6. **Add Balance**: Same process as providers
7. **Withdraw**: Same process as providers (minimum ₹150)
8. **Refer & Earn**: Share your referral code
   - Earn ₹50 for each new user
9. **Notifications**: Receive Telegram messages when:
   - Tasks are approved (with payment confirmation)
   - Tasks are rejected (with reason)

### For Admins

1. **Access**: Your Telegram UID must be set in `ADMIN_TELEGRAM_UID`
2. **Approve Transactions**: Review deposit/withdrawal requests
3. **Approve Tasks**: Verify worker submissions
4. **Manage Payment Info**: Update UPI ID and Crypto wallet
5. **View Analytics**: Monitor users, tasks, referrals

## File Upload Guidelines

### Documents
- Formats: PDF, DOCX, PPT, PNG, JPG
- Max Size: 300 KB
- Use for: Screenshots, certificates, reports

### Videos
- Formats: MP4, AVI, MKV
- Max Size: 10 MB
- Use for: Task demonstrations, proof videos

## Wallet Flow

### Deposit (Add Balance)
1. User clicks "Add Balance"
2. Enters amount (₹1 - ₹10,000)
3. Selects payment method (UPI/Crypto)
4. Bot shows payment details (QR code for UPI, wallet address for Crypto)
5. After 2 minutes, user enters UTR/Transaction ID
6. Admin approves/rejects in admin dashboard
7. Balance updated upon approval

### Withdrawal
1. User clicks "Withdraw" (minimum ₹150)
2. Selects method (UPI/Bank/Crypto)
3. Enters payment details
4. Enters amount (deducted immediately)
5. Admin processes withdrawal manually
6. If rejected, amount is refunded

## Notification System

The bot sends real-time Telegram notifications for key events:

### For Providers:
- **Task Submission**: Receive message when a worker submits proof for your task
  - Includes worker name and task title
  - Prompts to review and approve in dashboard

### For Workers/Takers:
- **Task Approved**: Receive congratulations message with payment confirmation
  - Shows task title and reward amount
  - Confirms wallet credit
- **Task Rejected**: Receive notification with rejection reason
  - Explains why submission was rejected
  - Allows opportunity to resubmit if applicable

### Automatic Processes:
- **Payment Approval**: Instant wallet balance update upon task approval
- **Referral Bonus**: Automatic ₹50 credit when referred user registers
- **Transaction Updates**: Real-time status updates for deposits/withdrawals

## Security Features

- Channel membership verification
- Password hashing (SHA-256)
- Admin-only access controls
- Transaction verification system
- File size limits to prevent abuse

## Troubleshooting

### Bot doesn't respond
- Check if bot token is correct
- Ensure bot.py is running
- Check internet connection

### Database errors
- Verify Supabase URL and key
- Ensure schema is properly executed
- Check Supabase dashboard for errors

### Channel verification fails
- Ensure bot is admin in the channel
- Check channel ID format (@channelname)
- Verify user has joined the channel

### File upload fails
- Check file size limits
- Ensure Supabase storage buckets exist
- Verify storage policies

## Development

### Project Structure
```
telegram-workhub-bot/
├── bot.py                  # Main bot application
├── config.py              # Configuration settings
├── database.py            # Database operations
├── utils.py               # Utility functions
├── handlers/              # Command and callback handlers
│   ├── __init__.py
│   ├── start.py          # Start and verification
│   ├── provider.py       # Provider features
│   ├── taker.py          # Worker features
│   ├── wallet.py         # Wallet operations
│   ├── admin.py          # Admin dashboard
│   └── support.py        # Support system
├── requirements.txt       # Python dependencies
├── supabase_schema.sql   # Database schema
├── .env.example          # Environment template
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

### Adding New Features

1. Create handler in `handlers/` directory
2. Add conversation states in handler file
3. Register handlers in `bot.py`
4. Update database schema if needed
5. Test thoroughly

## Maintenance

### Regular Tasks
- Monitor wallet transactions
- Review support messages
- Check task submissions
- Update payment information
- Backup Supabase database

### Monitoring
- Check bot logs for errors
- Monitor Supabase usage
- Track user registrations
- Review transaction patterns

## Support & Contributing

For questions or issues:
1. Check this README
2. Review Supabase logs
3. Check bot.py logs
4. Open an issue on GitHub (if applicable)

## License

This project is open-source. Feel free to modify and use for your needs.

## Disclaimer

This bot handles financial transactions. Ensure you:
- Comply with local regulations
- Implement proper security measures
- Keep backups of database
- Monitor for fraudulent activities
- Have clear terms & conditions for users

## Credits

Built with:
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- [Supabase](https://supabase.com)
- Python community libraries

---

**Happy Bot Building! 🚀**
