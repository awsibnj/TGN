from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
import database as db
import config
import utils
from datetime import datetime

TAKER_NAME, TAKER_MOBILE, TAKER_DOB, TAKER_PASSWORD, TAKER_CONFIRM_PASSWORD, TAKER_REFERRAL = range(6)
SUBMIT_PROOF_DOC, SUBMIT_PROOF_VIDEO = range(2)

async def register_taker_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user = update.effective_user
    existing_user = db.get_user_by_telegram_uid(user.id)
    
    if existing_user and existing_user.get('name') and existing_user.get('mobile'):
        await query.edit_message_text("✅ You are already registered!")
        return ConversationHandler.END
    
    await query.edit_message_text(
        "📝 **Work Taker Registration**\n\n"
        "Let's get you registered to start earning!\n\n"
        "Please enter your **full name**:",
        parse_mode='Markdown'
    )
    return TAKER_NAME

async def taker_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['taker_name'] = update.message.text
    await update.message.reply_text(
        "📱 Please enter your **mobile number**:",
        parse_mode='Markdown'
    )
    return TAKER_MOBILE

async def taker_mobile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mobile = update.message.text
    
    if not utils.validate_mobile(mobile):
        await update.message.reply_text(
            "❌ Invalid mobile number. Please enter a valid mobile number:",
            parse_mode='Markdown'
        )
        return TAKER_MOBILE
    
    context.user_data['taker_mobile'] = mobile
    await update.message.reply_text(
        "📅 Please enter your **date of birth** (Format: YYYY-MM-DD):",
        parse_mode='Markdown'
    )
    return TAKER_DOB

async def taker_dob(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dob = update.message.text
    
    try:
        datetime.strptime(dob, '%Y-%m-%d')
        context.user_data['taker_dob'] = dob
    except:
        await update.message.reply_text(
            "❌ Invalid date format. Please enter date as YYYY-MM-DD:",
            parse_mode='Markdown'
        )
        return TAKER_DOB
    
    await update.message.reply_text(
        "🔒 Create a **password** for your account:",
        parse_mode='Markdown'
    )
    return TAKER_PASSWORD

async def taker_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    password = update.message.text
    
    if len(password) < 6:
        await update.message.reply_text(
            "❌ Password must be at least 6 characters. Please try again:",
            parse_mode='Markdown'
        )
        return TAKER_PASSWORD
    
    context.user_data['taker_password'] = password
    await update.message.reply_text(
        "🔒 **Confirm your password**:",
        parse_mode='Markdown'
    )
    return TAKER_CONFIRM_PASSWORD

async def taker_confirm_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    confirm_password = update.message.text
    
    if confirm_password != context.user_data['taker_password']:
        await update.message.reply_text(
            "❌ Passwords don't match. Please enter password again:",
            parse_mode='Markdown'
        )
        context.user_data.pop('taker_password', None)
        return TAKER_PASSWORD
    
    await update.message.reply_text(
        "🎁 Enter **referral code** (if any) or type 'skip':",
        parse_mode='Markdown'
    )
    return TAKER_REFERRAL

async def taker_referral(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    
    password_hash = db.hash_password(context.user_data['taker_password'])
    
    updates = {
        'name': context.user_data['taker_name'],
        'mobile': context.user_data['taker_mobile'],
        'dob': context.user_data['taker_dob'],
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
        "You are now registered as a Work Taker!\n"
        "Use /start to access your dashboard and start earning!",
        parse_mode='Markdown'
    )
    
    return ConversationHandler.END

async def cancel_taker_registration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        "❌ Registration cancelled. Use /start to try again.",
        parse_mode='Markdown'
    )
    return ConversationHandler.END

async def get_new_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    categories = db.get_all_categories()
    keyboard = [[InlineKeyboardButton("🌟 All Tasks", callback_data="view_tasks_all")]]
    
    for cat in categories:
        keyboard.append([InlineKeyboardButton(f"{cat['name']}", callback_data=f"view_tasks_{cat['id']}")])
    
    keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="back_to_menu")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "🎯 **Get New Task**\n\n"
        "Select a category to view available tasks:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def view_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    category_id = query.data.replace('view_tasks_', '')
    
    if category_id == 'all':
        tasks = db.get_available_tasks()
    else:
        tasks = db.get_available_tasks(category_id)
    
    if not tasks:
        await query.edit_message_text(
            "📭 No tasks available in this category right now.\n\n"
            "Check back later!",
            parse_mode='Markdown'
        )
        return
    
    text = "🎯 **Available Tasks**\n\n"
    keyboard = []
    
    for task in tasks[:10]:
        category_name = task.get('categories', {}).get('name', 'N/A') if task.get('categories') else 'N/A'
        provider_name = task.get('users', {}).get('name', 'Unknown') if task.get('users') else 'Unknown'
        available_slots = task['total_slots'] - task['filled_slots']
        
        text += (
            f"**{task['title']}**\n"
            f"📂 {category_name} | 💰 ₹{task['reward']}\n"
            f"👔 Provider: {provider_name}\n"
            f"👥 Slots: {available_slots}/{task['total_slots']} available\n"
            f"📋 {task['description'][:100]}...\n\n"
        )
        
        keyboard.append([InlineKeyboardButton(f"Take: {task['title'][:30]}...", callback_data=f"take_task_{task['id']}")])
    
    keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="taker_get_task")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def take_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    task_id = query.data.replace('take_task_', '')
    user = update.effective_user
    existing_user = db.get_user_by_telegram_uid(user.id)
    
    task = db.get_task_by_id(task_id)
    
    if not task:
        await query.edit_message_text("❌ Task not found or no longer available.")
        return
    
    if task['filled_slots'] >= task['total_slots']:
        await query.edit_message_text("❌ This task is already full.")
        return
    
    assignment = db.create_task_assignment(task_id, existing_user['id'])
    
    if assignment:
        await query.edit_message_text(
            f"✅ **Task Accepted!**\n\n"
            f"Task: {task['title']}\n"
            f"Reward: ₹{task['reward']}\n\n"
            f"Requirements:\n{task.get('requirements', 'N/A')}\n\n"
            f"Complete the task and submit proof in 'My Tasks'.",
            parse_mode='Markdown'
        )
    else:
        await query.edit_message_text(
            "❌ Error accepting task. You may have already accepted this task.",
            parse_mode='Markdown'
        )

async def my_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user = update.effective_user
    existing_user = db.get_user_by_telegram_uid(user.id)
    
    assignments = db.get_task_assignments_by_taker(existing_user['id'])
    
    if not assignments:
        await query.edit_message_text(
            "📝 **My Tasks**\n\n"
            "You haven't accepted any tasks yet.",
            parse_mode='Markdown'
        )
        return
    
    text = "📝 **My Tasks**\n\n"
    keyboard = []
    
    for assignment in assignments[:10]:
        task = assignment.get('tasks', {})
        status_emoji = {
            'accepted': '🆕',
            'submitted': '⏳',
            'approved': '✅',
            'rejected': '❌'
        }.get(assignment['status'], '❓')
        
        text += (
            f"{status_emoji} **{task.get('title', 'N/A')}**\n"
            f"   Reward: ₹{task.get('reward', 0)}\n"
            f"   Status: {assignment['status'].upper()}\n\n"
        )
        
        if assignment['status'] == 'accepted':
            keyboard.append([InlineKeyboardButton(f"Submit: {task.get('title', 'Task')[:25]}...", callback_data=f"submit_task_{assignment['id']}")])
    
    keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="back_to_menu")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def submit_task_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    assignment_id = query.data.replace('submit_task_', '')
    context.user_data['assignment_id'] = assignment_id
    
    await query.edit_message_text(
        "📎 **Submit Task Proof**\n\n"
        "Please upload a **document** (PDF, DOCX, PPT, PNG, JPG)\n"
        "Max size: 300 KB\n\n"
        "Or type 'skip' to skip document upload.",
        parse_mode='Markdown'
    )
    
    return SUBMIT_PROOF_DOC

async def submit_proof_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text and update.message.text.lower() == 'skip':
        context.user_data['proof_doc_url'] = None
        await update.message.reply_text(
            "📹 Now upload a **video** (MP4, AVI, MKV)\n"
            "Max size: 10 MB\n\n"
            "Or type 'skip' to skip video upload.",
            parse_mode='Markdown'
        )
        return SUBMIT_PROOF_VIDEO
    
    if not update.message.document:
        await update.message.reply_text(
            "❌ Please upload a document or type 'skip'.",
            parse_mode='Markdown'
        )
        return SUBMIT_PROOF_DOC
    
    document = update.message.document
    
    if document.file_size > config.MAX_DOCUMENT_SIZE:
        await update.message.reply_text(
            f"❌ File too large! Max size: {config.MAX_DOCUMENT_SIZE / 1024} KB",
            parse_mode='Markdown'
        )
        return SUBMIT_PROOF_DOC
    
    try:
        file = await context.bot.get_file(document.file_id)
        file_bytes = await file.download_as_bytearray()
        
        assignment_id = context.user_data['assignment_id']
        user = update.effective_user
        file_path = f"{user.id}/{assignment_id}_{document.file_name}"
        
        file_url = db.upload_file_to_storage(bytes(file_bytes), 'task-documents', file_path)
        
        if not file_url:
            file_url = file.file_path
    except Exception as e:
        print(f"Error uploading document to storage: {e}")
        file = await context.bot.get_file(document.file_id)
        file_url = file.file_path
    
    context.user_data['proof_doc_url'] = file_url
    
    await update.message.reply_text(
        "✅ Document received!\n\n"
        "📹 Now upload a **video** (MP4, AVI, MKV)\n"
        "Max size: 10 MB\n\n"
        "Or type 'skip' to skip video upload.",
        parse_mode='Markdown'
    )
    return SUBMIT_PROOF_VIDEO

async def submit_proof_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text and update.message.text.lower() == 'skip':
        context.user_data['proof_video_url'] = None
    elif update.message.video:
        video = update.message.video
        
        if video.file_size > config.MAX_VIDEO_SIZE:
            await update.message.reply_text(
                f"❌ Video too large! Max size: {config.MAX_VIDEO_SIZE / (1024 * 1024)} MB",
                parse_mode='Markdown'
            )
            return SUBMIT_PROOF_VIDEO
        
        try:
            file = await context.bot.get_file(video.file_id)
            file_bytes = await file.download_as_bytearray()
            
            assignment_id = context.user_data['assignment_id']
            user = update.effective_user
            file_ext = video.file_name.split('.')[-1] if video.file_name else 'mp4'
            file_path = f"{user.id}/{assignment_id}_video.{file_ext}"
            
            file_url = db.upload_file_to_storage(bytes(file_bytes), 'task-videos', file_path)
            
            if not file_url:
                file_url = file.file_path
        except Exception as e:
            print(f"Error uploading video to storage: {e}")
            file = await context.bot.get_file(video.file_id)
            file_url = file.file_path
        
        context.user_data['proof_video_url'] = file_url
    else:
        await update.message.reply_text(
            "❌ Please upload a video or type 'skip'.",
            parse_mode='Markdown'
        )
        return SUBMIT_PROOF_VIDEO
    
    assignment_id = context.user_data['assignment_id']
    proof_doc_url = context.user_data.get('proof_doc_url')
    proof_video_url = context.user_data.get('proof_video_url')
    
    if not proof_doc_url and not proof_video_url:
        await update.message.reply_text(
            "❌ You must upload at least one proof (document or video).",
            parse_mode='Markdown'
        )
        context.user_data.clear()
        return ConversationHandler.END
    
    updates = {
        'status': 'submitted',
        'submitted_at': datetime.utcnow().isoformat(),
        'proof_file_url': proof_doc_url,
        'proof_video_url': proof_video_url
    }
    
    db.update_task_assignment(assignment_id, updates)
    
    assignment = db.get_all_task_assignments()
    assignment_data = next((a for a in assignment if a['id'] == assignment_id), None)
    
    if assignment_data:
        task = db.get_task_by_id(assignment_data['task_id'])
        if task and task.get('users'):
            provider_telegram_uid = task['users']['telegram_uid']
            user = update.effective_user
            existing_user = db.get_user_by_telegram_uid(user.id)
            
            try:
                await context.bot.send_message(
                    chat_id=provider_telegram_uid,
                    text=f"📬 **New Task Submission**\n\n"
                         f"Work taker **{existing_user.get('name', 'Unknown')}** has submitted proof for task:\n"
                         f"**{task['title']}**\n\n"
                         f"Please review and approve in your admin/provider dashboard.",
                    parse_mode='Markdown'
                )
            except Exception as e:
                print(f"Error sending notification to provider: {e}")
    
    await update.message.reply_text(
        "✅ **Task Submitted Successfully!**\n\n"
        "Your proof has been submitted for review.\n"
        "You'll receive payment once approved.",
        parse_mode='Markdown'
    )
    
    context.user_data.clear()
    return ConversationHandler.END

async def taker_refer(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

async def cancel_submission(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        "❌ Submission cancelled. Use /start to access your dashboard.",
        parse_mode='Markdown'
    )
    return ConversationHandler.END
