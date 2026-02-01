from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
import database as db
import utils
import config
from datetime import datetime

PROVIDER_NAME, PROVIDER_MOBILE, PROVIDER_EMAIL, PROVIDER_GENDER, PROVIDER_DOB, PROVIDER_LOCATION, PROVIDER_PASSWORD, PROVIDER_CONFIRM_PASSWORD, PROVIDER_REFERRAL = range(9)
TASK_TITLE, TASK_DESCRIPTION, TASK_CATEGORY, TASK_REWARD, TASK_SLOTS, TASK_REQUIREMENTS = range(6)

async def register_provider_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user = update.effective_user
    existing_user = db.get_user_by_telegram_uid(user.id)
    
    if existing_user and existing_user['role'] == 'provider':
        await query.edit_message_text("✅ You are already registered as a Provider!")
        return ConversationHandler.END
    
    await query.edit_message_text(
        "📝 **Provider Registration**\n\n"
        "Let's get you registered as a Work Provider!\n\n"
        "Please enter your **full name**:",
        parse_mode='Markdown'
    )
    return PROVIDER_NAME

async def provider_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['provider_name'] = update.message.text
    await update.message.reply_text(
        "📱 Please enter your **mobile number**:",
        parse_mode='Markdown'
    )
    return PROVIDER_MOBILE

async def provider_mobile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mobile = update.message.text
    
    if not utils.validate_mobile(mobile):
        await update.message.reply_text(
            "❌ Invalid mobile number. Please enter a valid mobile number:",
            parse_mode='Markdown'
        )
        return PROVIDER_MOBILE
    
    context.user_data['provider_mobile'] = mobile
    await update.message.reply_text(
        "📧 Please enter your **email address**:",
        parse_mode='Markdown'
    )
    return PROVIDER_EMAIL

async def provider_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    email = update.message.text
    
    if not utils.validate_email(email):
        await update.message.reply_text(
            "❌ Invalid email. Please enter a valid email address:",
            parse_mode='Markdown'
        )
        return PROVIDER_EMAIL
    
    context.user_data['provider_email'] = email
    
    keyboard = [
        [InlineKeyboardButton("Male", callback_data="gender_male")],
        [InlineKeyboardButton("Female", callback_data="gender_female")],
        [InlineKeyboardButton("Other", callback_data="gender_other")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "👤 Please select your **gender**:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
    return PROVIDER_GENDER

async def provider_gender(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    gender = query.data.replace('gender_', '').capitalize()
    context.user_data['provider_gender'] = gender
    
    await query.edit_message_text(
        f"Selected: {gender}\n\n"
        "📅 Please enter your **date of birth** (Format: YYYY-MM-DD):",
        parse_mode='Markdown'
    )
    return PROVIDER_DOB

async def provider_dob(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dob = update.message.text
    
    try:
        datetime.strptime(dob, '%Y-%m-%d')
        context.user_data['provider_dob'] = dob
    except:
        await update.message.reply_text(
            "❌ Invalid date format. Please enter date as YYYY-MM-DD:",
            parse_mode='Markdown'
        )
        return PROVIDER_DOB
    
    await update.message.reply_text(
        "📍 Please enter your **location** (City, State):",
        parse_mode='Markdown'
    )
    return PROVIDER_LOCATION

async def provider_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['provider_location'] = update.message.text
    await update.message.reply_text(
        "🔒 Create a **password** for your account:",
        parse_mode='Markdown'
    )
    return PROVIDER_PASSWORD

async def provider_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    password = update.message.text
    
    if len(password) < 6:
        await update.message.reply_text(
            "❌ Password must be at least 6 characters. Please try again:",
            parse_mode='Markdown'
        )
        return PROVIDER_PASSWORD
    
    context.user_data['provider_password'] = password
    await update.message.reply_text(
        "🔒 **Confirm your password**:",
        parse_mode='Markdown'
    )
    return PROVIDER_CONFIRM_PASSWORD

async def provider_confirm_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    confirm_password = update.message.text
    
    if confirm_password != context.user_data['provider_password']:
        await update.message.reply_text(
            "❌ Passwords don't match. Please enter password again:",
            parse_mode='Markdown'
        )
        context.user_data.pop('provider_password', None)
        return PROVIDER_PASSWORD
    
    await update.message.reply_text(
        "🎁 Enter **referral code** (if any) or type 'skip':",
        parse_mode='Markdown'
    )
    return PROVIDER_REFERRAL

async def provider_referral(update: Update, context: ContextTypes.DEFAULT_TYPE):
    referral_code = update.message.text.strip()
    user = update.effective_user
    existing_user = db.get_user_by_telegram_uid(user.id)
    
    referrer_id = None
    if referral_code.lower() != 'skip':
        referrer = db.get_user_by_referral_code(referral_code)
        if referrer:
            referrer_id = referrer['id']
        else:
            await update.message.reply_text(
                "⚠️ Invalid referral code. Proceeding without referral...",
                parse_mode='Markdown'
            )
    
    password_hash = db.hash_password(context.user_data['provider_password'])
    
    updates = {
        'role': 'provider',
        'name': context.user_data['provider_name'],
        'mobile': context.user_data['provider_mobile'],
        'email': context.user_data['provider_email'],
        'gender': context.user_data['provider_gender'],
        'dob': context.user_data['provider_dob'],
        'location': context.user_data['provider_location'],
        'password_hash': password_hash
    }
    
    if referrer_id:
        updates['referred_by'] = referrer_id
    
    db.update_user(existing_user['id'], updates)
    
    if referrer_id:
        db.create_referral(referrer_id, existing_user['id'])
    
    context.user_data.clear()
    
    await update.message.reply_text(
        "✅ **Registration Successful!**\n\n"
        "You are now registered as a Work Provider!\n"
        "Use /start to access your dashboard.",
        parse_mode='Markdown'
    )
    
    return ConversationHandler.END

async def cancel_registration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        "❌ Registration cancelled. Use /start to try again.",
        parse_mode='Markdown'
    )
    return ConversationHandler.END

async def create_task_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        "📝 **Create New Task**\n\n"
        "Let's create a new task for workers!\n\n"
        "Please enter the **task title**:",
        parse_mode='Markdown'
    )
    return TASK_TITLE

async def task_title(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['task_title'] = update.message.text
    await update.message.reply_text(
        "📄 Please enter the **task description**:",
        parse_mode='Markdown'
    )
    return TASK_DESCRIPTION

async def task_description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['task_description'] = update.message.text
    
    categories = db.get_all_categories()
    keyboard = []
    for cat in categories:
        keyboard.append([InlineKeyboardButton(cat['name'], callback_data=f"cat_{cat['id']}")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "📂 Please select a **category**:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
    return TASK_CATEGORY

async def task_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    category_id = query.data.replace('cat_', '')
    context.user_data['task_category'] = category_id
    
    await query.edit_message_text(
        "💰 Enter the **reward amount** per worker (in ₹):",
        parse_mode='Markdown'
    )
    return TASK_REWARD

async def task_reward(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        reward = float(update.message.text)
        if reward <= 0:
            raise ValueError
        context.user_data['task_reward'] = reward
    except:
        await update.message.reply_text(
            "❌ Invalid amount. Please enter a valid number:",
            parse_mode='Markdown'
        )
        return TASK_REWARD
    
    await update.message.reply_text(
        "👥 How many **workers** do you need for this task?",
        parse_mode='Markdown'
    )
    return TASK_SLOTS

async def task_slots(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        slots = int(update.message.text)
        if slots <= 0:
            raise ValueError
        context.user_data['task_slots'] = slots
    except:
        await update.message.reply_text(
            "❌ Invalid number. Please enter a valid number:",
            parse_mode='Markdown'
        )
        return TASK_SLOTS
    
    await update.message.reply_text(
        "📋 Enter any **special requirements** or instructions for workers:",
        parse_mode='Markdown'
    )
    return TASK_REQUIREMENTS

async def task_requirements(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['task_requirements'] = update.message.text
    
    user = update.effective_user
    existing_user = db.get_user_by_telegram_uid(user.id)
    
    total_cost = context.user_data['task_reward'] * context.user_data['task_slots']
    current_balance = float(existing_user.get('wallet_balance', 0))
    
    if current_balance < total_cost:
        await update.message.reply_text(
            f"❌ **Insufficient Balance!**\n\n"
            f"Task Cost: ₹{total_cost:,.2f}\n"
            f"Your Balance: ₹{current_balance:,.2f}\n\n"
            f"Please add ₹{total_cost - current_balance:,.2f} to your wallet.",
            parse_mode='Markdown'
        )
        context.user_data.clear()
        return ConversationHandler.END
    
    task = db.create_task(
        provider_id=existing_user['id'],
        title=context.user_data['task_title'],
        description=context.user_data['task_description'],
        category_id=context.user_data['task_category'],
        reward=context.user_data['task_reward'],
        total_slots=context.user_data['task_slots'],
        requirements=context.user_data['task_requirements']
    )
    
    if task:
        db.update_wallet_balance(existing_user['id'], -total_cost)
        db.create_wallet_transaction(
            existing_user['id'],
            'task_deduction',
            total_cost,
            payment_method='task_creation',
            payment_details={'task_id': task['id']}
        )
        
        await update.message.reply_text(
            f"✅ **Task Created Successfully!**\n\n"
            f"Title: {task['title']}\n"
            f"Reward: ₹{task['reward']}\n"
            f"Workers: {task['total_slots']}\n"
            f"Total Cost: ₹{total_cost:,.2f}\n\n"
            f"Remaining Balance: ₹{current_balance - total_cost:,.2f}",
            parse_mode='Markdown'
        )
    else:
        await update.message.reply_text(
            "❌ Error creating task. Please try again.",
            parse_mode='Markdown'
        )
    
    context.user_data.clear()
    return ConversationHandler.END

async def view_provider_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user = update.effective_user
    existing_user = db.get_user_by_telegram_uid(user.id)
    
    tasks = db.get_tasks_by_provider(existing_user['id'])
    
    if not tasks:
        await query.edit_message_text(
            "📋 **My Tasks**\n\n"
            "You haven't created any tasks yet.",
            parse_mode='Markdown'
        )
        return
    
    text = "📋 **My Tasks**\n\n"
    for i, task in enumerate(tasks[:10], 1):
        category_name = task.get('categories', {}).get('name', 'N/A') if task.get('categories') else 'N/A'
        text += (
            f"{i}. **{task['title']}**\n"
            f"   Category: {category_name}\n"
            f"   Reward: ₹{task['reward']} × {task['filled_slots']}/{task['total_slots']} workers\n"
            f"   Status: {task['status'].upper()}\n\n"
        )
    
    await query.edit_message_text(text, parse_mode='Markdown')

async def provider_refer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user = update.effective_user
    existing_user = db.get_user_by_telegram_uid(user.id)
    
    referral_code = existing_user['referral_code']
    referrals = db.get_referrals_by_referrer(existing_user['id'])
    
    text = (
        f"🎁 **Refer & Earn**\n\n"
        f"Your Referral Code: `{referral_code}`\n\n"
        f"Share your code and earn ₹{config.REFERRAL_BONUS} for each new user!\n\n"
        f"Total Referrals: {len(referrals)}\n"
        f"Total Earned: ₹{len(referrals) * config.REFERRAL_BONUS}\n\n"
        f"Share this message:\n"
        f"Join WorkHub and start earning! Use my referral code: {referral_code}"
    )
    
    await query.edit_message_text(text, parse_mode='Markdown')

async def provider_campaign(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user = update.effective_user
    existing_user = db.get_user_by_telegram_uid(user.id)
    
    tasks = db.get_tasks_by_provider(existing_user['id'])
    active_tasks = [t for t in tasks if t['status'] == 'available']
    
    total_slots = sum(t['total_slots'] for t in active_tasks)
    filled_slots = sum(t['filled_slots'] for t in active_tasks)
    total_budget = sum(float(t['reward']) * t['total_slots'] for t in active_tasks)
    
    text = (
        f"📢 **Campaign Management**\n\n"
        f"Active Campaigns: {len(active_tasks)}\n"
        f"Total Slots: {filled_slots}/{total_slots}\n"
        f"Total Budget: ₹{total_budget:,.2f}\n\n"
        f"**Campaign Performance:**\n"
    )
    
    for i, task in enumerate(active_tasks[:5], 1):
        category_name = task.get('categories', {}).get('name', 'N/A') if task.get('categories') else 'N/A'
        completion_rate = (task['filled_slots'] / task['total_slots'] * 100) if task['total_slots'] > 0 else 0
        text += (
            f"\n{i}. **{task['title']}**\n"
            f"   Category: {category_name}\n"
            f"   Progress: {task['filled_slots']}/{task['total_slots']} ({completion_rate:.0f}%)\n"
            f"   Budget: ₹{float(task['reward']) * task['total_slots']:,.2f}\n"
        )
    
    if not active_tasks:
        text += "\nNo active campaigns. Create a new task to start!"
    
    keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="back_to_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def provider_lifetime_earn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user = update.effective_user
    existing_user = db.get_user_by_telegram_uid(user.id)
    
    transactions = db.get_wallet_transactions(existing_user['id'])
    tasks = db.get_tasks_by_provider(existing_user['id'])
    referrals = db.get_referrals_by_referrer(existing_user['id'])
    
    total_deposits = sum(float(t['amount']) for t in transactions if t['transaction_type'] == 'deposit' and t['status'] == 'approved')
    total_spent = sum(float(t['amount']) for t in transactions if t['transaction_type'] == 'task_deduction')
    total_withdrawals = sum(float(t['amount']) for t in transactions if t['transaction_type'] == 'withdrawal' and t['status'] == 'approved')
    referral_earnings = len(referrals) * config.REFERRAL_BONUS
    
    total_tasks_created = len(tasks)
    total_workers_hired = sum(t['filled_slots'] for t in tasks)
    
    text = (
        f"📊 **Lifetime Earnings & Stats**\n\n"
        f"💰 **Financial Summary:**\n"
        f"• Total Deposits: ₹{total_deposits:,.2f}\n"
        f"• Total Spent on Tasks: ₹{total_spent:,.2f}\n"
        f"• Total Withdrawals: ₹{total_withdrawals:,.2f}\n"
        f"• Referral Earnings: ₹{referral_earnings:,.2f}\n"
        f"• Current Balance: ₹{float(existing_user.get('wallet_balance', 0)):,.2f}\n\n"
        f"📈 **Activity Summary:**\n"
        f"• Tasks Created: {total_tasks_created}\n"
        f"• Workers Hired: {total_workers_hired}\n"
        f"• Referrals Made: {len(referrals)}\n\n"
        f"🎯 **ROI Metrics:**\n"
        f"• Average Task Cost: ₹{(total_spent / total_tasks_created if total_tasks_created > 0 else 0):,.2f}\n"
        f"• Average per Worker: ₹{(total_spent / total_workers_hired if total_workers_hired > 0 else 0):,.2f}\n"
    )
    
    keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="back_to_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
