from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
import database as db
import config

VERIFY_JOIN = 1

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    telegram_uid = user.id
    username = user.username or user.first_name
    
    existing_user = db.get_user_by_telegram_uid(telegram_uid)
    
    if not existing_user:
        db.create_user(telegram_uid, username, role='taker', is_verified=False)
        existing_user = db.get_user_by_telegram_uid(telegram_uid)
    
    if telegram_uid == config.ADMIN_TELEGRAM_UID:
        if existing_user['role'] != 'admin':
            db.update_user(existing_user['id'], {'role': 'admin', 'is_verified': True})
            existing_user = db.get_user_by_telegram_uid(telegram_uid)
    
    welcome_text = f"""
🌟 **Welcome to WorkHub Bot!** 🌟

Hello {user.first_name}! 👋

Your one-stop solution for connecting **Work Providers** and **Work Takers**.

✨ **What can you do here?**
• Post tasks and find workers
• Complete tasks and earn money
• Manage your wallet
• Refer friends and earn bonuses

💼 **Get Started:**
First, join our official channel to unlock all features!
"""
    
    if not existing_user['is_verified']:
        keyboard = [
            [InlineKeyboardButton("📢 Join Channel", url=f"https://t.me/{config.TELEGRAM_CHANNEL_ID.replace('@', '')}")],
            [InlineKeyboardButton("✅ Verify Join", callback_data="verify_join")],
            [InlineKeyboardButton("📜 Read Terms & Conditions", callback_data="read_terms")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')
    else:
        await show_main_menu(update, context, existing_user)

async def verify_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user = update.effective_user
    telegram_uid = user.id
    
    try:
        member = await context.bot.get_chat_member(config.TELEGRAM_CHANNEL_ID, telegram_uid)
        
        if member.status in ['member', 'administrator', 'creator']:
            db.verify_user(telegram_uid)
            existing_user = db.get_user_by_telegram_uid(telegram_uid)
            
            await query.edit_message_text(
                "✅ **Channel membership verified!**\n\n"
                "Welcome to WorkHub! You now have full access to all features.",
                parse_mode='Markdown'
            )
            
            await show_main_menu(update, context, existing_user)
        else:
            await query.edit_message_text(
                "❌ **Not verified!**\n\n"
                "Please join the channel first, then click Verify Join.",
                parse_mode='Markdown'
            )
            keyboard = [
                [InlineKeyboardButton("📢 Join Channel", url=f"https://t.me/{config.TELEGRAM_CHANNEL_ID.replace('@', '')}")],
                [InlineKeyboardButton("✅ Verify Join", callback_data="verify_join")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.message.reply_text("Please try again:", reply_markup=reply_markup)
    except Exception as e:
        await query.edit_message_text(
            f"⚠️ **Error verifying membership**\n\n"
            f"Please make sure you've joined {config.TELEGRAM_CHANNEL_NAME} and try again.",
            parse_mode='Markdown'
        )
        keyboard = [
            [InlineKeyboardButton("📢 Join Channel", url=f"https://t.me/{config.TELEGRAM_CHANNEL_ID.replace('@', '')}")],
            [InlineKeyboardButton("✅ Verify Join", callback_data="verify_join")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text("Please try again:", reply_markup=reply_markup)

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, user_data):
    role = user_data['role']
    
    if role == 'admin':
        keyboard = [
            [InlineKeyboardButton("👥 View All Users", callback_data="admin_users")],
            [InlineKeyboardButton("📋 View All Tasks", callback_data="admin_tasks")],
            [InlineKeyboardButton("✅ Approve Transactions", callback_data="admin_transactions")],
            [InlineKeyboardButton("💬 Support Messages", callback_data="admin_support")],
            [InlineKeyboardButton("⚙️ Manage Payment Info", callback_data="admin_payment_info")],
            [InlineKeyboardButton("📂 Manage Categories", callback_data="admin_categories")],
            [InlineKeyboardButton("📊 View Referrals", callback_data="admin_referrals")],
            [InlineKeyboardButton("✔️ Approve Task Proofs", callback_data="admin_approve_proofs")]
        ]
        text = f"🔧 **Admin Dashboard**\n\nWelcome back, Admin!"
    elif role == 'provider':
        keyboard = [
            [InlineKeyboardButton("➕ Create New Task", callback_data="provider_create_task")],
            [InlineKeyboardButton("📋 View My Tasks", callback_data="provider_view_tasks")],
            [InlineKeyboardButton("💰 Wallet", callback_data="provider_wallet")],
            [InlineKeyboardButton("🎁 Refer & Earn", callback_data="provider_refer")],
            [InlineKeyboardButton("📢 Run Campaign", callback_data="provider_campaign")],
            [InlineKeyboardButton("📊 Lifetime Earn", callback_data="provider_lifetime_earn")],
            [InlineKeyboardButton("💬 Support", callback_data="provider_support")]
        ]
        balance = user_data.get('wallet_balance', 0)
        text = f"👔 **Provider Dashboard**\n\nWelcome back, {user_data['name'] or 'Provider'}!\n💰 Balance: {format_currency(balance)}"
    else:
        if not user_data.get('name') or not user_data.get('mobile'):
            keyboard = [
                [InlineKeyboardButton("📝 Complete Registration", callback_data="register_taker")],
                [InlineKeyboardButton("👔 Register as Provider", callback_data="register_provider")],
                [InlineKeyboardButton("📜 Read Terms & Conditions", callback_data="read_terms")],
                [InlineKeyboardButton("💬 Support", callback_data="taker_support")]
            ]
            text = f"🎯 **Welcome, {update.effective_user.first_name}!**\n\nPlease complete your registration to start earning!"
        else:
            keyboard = [
                [InlineKeyboardButton("🎯 Get New Task", callback_data="taker_get_task")],
                [InlineKeyboardButton("📝 My Tasks", callback_data="taker_my_tasks")],
                [InlineKeyboardButton("💰 Wallet", callback_data="taker_wallet")],
                [InlineKeyboardButton("🎁 Refer & Earn", callback_data="taker_refer")],
                [InlineKeyboardButton("💬 Support", callback_data="taker_support")],
                [InlineKeyboardButton("👔 Register as Provider", callback_data="register_provider")]
            ]
            balance = user_data.get('wallet_balance', 0)
            name = user_data.get('name') or update.effective_user.first_name
            text = f"🎯 **Work Taker Dashboard**\n\nWelcome back, {name}!\n💰 Balance: {format_currency(balance)}"
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        await update.callback_query.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    else:
        await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')

def format_currency(amount):
    return f"₹{float(amount):,.2f}"

async def read_terms(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    terms_text = """
📜 **Terms & Conditions**

**1. User Responsibilities**
• Provide accurate information
• Maintain account security
• Not share your account

**2. Work Providers**
• Post only legitimate tasks
• Maintain sufficient balance
• Pay workers promptly

**3. Work Takers**
• Complete tasks honestly
• Submit genuine proof
• Not attempt fraud

**4. Wallet & Payments**
• Min deposit: ₹1, Max: ₹10,000
• Min withdrawal: ₹150
• Subject to admin verification
• Processing: 24-48 hours

**5. Referral Program**
• Earn ₹50 per valid referral
• Cannot refer fake accounts

**6. Prohibited Activities**
• Multiple accounts
• Fraudulent activities
• Harassment or spam

**7. Account Termination**
We reserve the right to suspend/terminate accounts for violations.

By using WorkHub, you agree to these terms.

Full terms: [Contact Support]
"""
    
    keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="back_to_start")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(terms_text, reply_markup=reply_markup, parse_mode='Markdown')

async def back_to_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user = update.effective_user
    existing_user = db.get_user_by_telegram_uid(user.id)
    
    if not existing_user['is_verified']:
        welcome_text = f"""
🌟 **Welcome to WorkHub Bot!** 🌟

Hello {user.first_name}! 👋

Your one-stop solution for connecting **Work Providers** and **Work Takers**.

✨ **What can you do here?**
• Post tasks and find workers
• Complete tasks and earn money
• Manage your wallet
• Refer friends and earn bonuses

💼 **Get Started:**
First, join our official channel to unlock all features!
"""
        keyboard = [
            [InlineKeyboardButton("📢 Join Channel", url=f"https://t.me/{config.TELEGRAM_CHANNEL_ID.replace('@', '')}")],
            [InlineKeyboardButton("✅ Verify Join", callback_data="verify_join")],
            [InlineKeyboardButton("📜 Read Terms & Conditions", callback_data="read_terms")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')
    else:
        await show_main_menu(update, context, existing_user)
