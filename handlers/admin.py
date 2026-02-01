from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
import database as db
import utils

ADMIN_APPROVE_TXN, ADMIN_REJECT_TXN, ADMIN_REPLY_SUPPORT, ADMIN_UPDATE_UPI, ADMIN_UPDATE_CRYPTO, ADMIN_ADD_CATEGORY = range(6)
ADMIN_APPROVE_PROOF, ADMIN_REJECT_PROOF = range(2)

async def admin_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    users = db.get_all_users()
    
    text = "👥 **All Users**\n\n"
    
    providers = [u for u in users if u['role'] == 'provider']
    takers = [u for u in users if u['role'] == 'taker']
    admins = [u for u in users if u['role'] == 'admin']
    
    text += f"📊 **Statistics:**\n"
    text += f"Total Users: {len(users)}\n"
    text += f"Providers: {len(providers)}\n"
    text += f"Workers: {len(takers)}\n"
    text += f"Admins: {len(admins)}\n\n"
    
    text += "**Recent Users:**\n"
    for user in users[:10]:
        verified = "✅" if user['is_verified'] else "❌"
        text += (
            f"{verified} {user.get('name', 'N/A')} (@{user.get('username', 'N/A')})\n"
            f"   Role: {user['role'].upper()} | Balance: ₹{float(user.get('wallet_balance', 0)):,.2f}\n\n"
        )
    
    keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="back_to_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def admin_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    tasks = db.get_all_tasks()
    
    text = "📋 **All Tasks**\n\n"
    text += f"Total Tasks: {len(tasks)}\n\n"
    
    for task in tasks[:10]:
        category_name = task.get('categories', {}).get('name', 'N/A') if task.get('categories') else 'N/A'
        provider_name = task.get('users', {}).get('name', 'Unknown') if task.get('users') else 'Unknown'
        
        text += (
            f"**{task['title']}**\n"
            f"Provider: {provider_name}\n"
            f"Category: {category_name}\n"
            f"Reward: ₹{task['reward']} × {task['filled_slots']}/{task['total_slots']}\n"
            f"Status: {task['status'].upper()}\n\n"
        )
    
    keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="back_to_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def admin_transactions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    transactions = db.get_pending_wallet_transactions()
    
    if not transactions:
        await query.edit_message_text(
            "✅ **Wallet Transactions**\n\n"
            "No pending transactions!",
            parse_mode='Markdown'
        )
        return
    
    text = "💰 **Pending Transactions**\n\n"
    keyboard = []
    
    for txn in transactions[:10]:
        user_name = txn.get('users', {}).get('name', 'Unknown') if txn.get('users') else 'Unknown'
        txn_type = txn['transaction_type'].replace('_', ' ').title()
        
        text += (
            f"**{user_name}** - {txn_type}\n"
            f"Amount: ₹{txn['amount']}\n"
            f"Method: {txn.get('payment_method', 'N/A')}\n"
            f"UTR: {txn.get('utr_transaction_id', 'N/A')}\n"
            f"Date: {utils.format_date(txn['created_at'])}\n\n"
        )
        
        keyboard.append([
            InlineKeyboardButton(f"✅ Approve #{txn['id'][:8]}", callback_data=f"approve_txn_{txn['id']}"),
            InlineKeyboardButton(f"❌ Reject #{txn['id'][:8]}", callback_data=f"reject_txn_{txn['id']}")
        ])
    
    keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="back_to_menu")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def approve_transaction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    txn_id = query.data.replace('approve_txn_', '')
    
    result = db.approve_wallet_transaction(txn_id, admin_note="Approved by admin")
    
    if result:
        await query.edit_message_text(
            "✅ **Transaction Approved!**\n\n"
            "User's wallet has been updated.",
            parse_mode='Markdown'
        )
    else:
        await query.edit_message_text(
            "❌ Error approving transaction.",
            parse_mode='Markdown'
        )

async def reject_transaction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    txn_id = query.data.replace('reject_txn_', '')
    
    result = db.reject_wallet_transaction(txn_id, admin_note="Rejected by admin")
    
    if result:
        await query.edit_message_text(
            "❌ **Transaction Rejected!**\n\n"
            "User has been notified.",
            parse_mode='Markdown'
        )
    else:
        await query.edit_message_text(
            "❌ Error rejecting transaction.",
            parse_mode='Markdown'
        )

async def admin_support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    messages = db.get_all_support_messages()
    
    if not messages:
        await query.edit_message_text(
            "💬 **Support Messages**\n\n"
            "No support messages!",
            parse_mode='Markdown'
        )
        return
    
    text = "💬 **Support Messages**\n\n"
    
    for msg in messages[:10]:
        user_name = msg.get('users', {}).get('name', 'Unknown') if msg.get('users') else 'Unknown'
        status_emoji = {'open': '🔴', 'replied': '✅', 'closed': '⚫'}.get(msg['status'], '❓')
        
        text += (
            f"{status_emoji} **{user_name}**\n"
            f"Message: {utils.truncate_text(msg['message'], 100)}\n"
            f"Date: {utils.format_date(msg['created_at'])}\n\n"
        )
    
    keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="back_to_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def admin_payment_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    upi_info = db.get_payment_info('upi')
    crypto_info = db.get_payment_info('crypto')
    
    text = "⚙️ **Payment Information**\n\n"
    
    if upi_info:
        upi_details = upi_info['details']
        text += f"**UPI:**\n"
        text += f"UPI ID: {upi_details.get('upi_id', 'Not set')}\n"
        text += f"QR Code: {'Set' if upi_details.get('qr_code_url') else 'Not set'}\n\n"
    
    if crypto_info:
        crypto_details = crypto_info['details']
        text += f"**Crypto:**\n"
        text += f"Wallet: {crypto_details.get('wallet_address', 'Not set')}\n"
        text += f"Network: {crypto_details.get('network', 'Not set')}\n\n"
    
    keyboard = [
        [InlineKeyboardButton("✏️ Update UPI", callback_data="update_upi")],
        [InlineKeyboardButton("✏️ Update Crypto", callback_data="update_crypto")],
        [InlineKeyboardButton("🔙 Back", callback_data="back_to_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def admin_categories(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    categories = db.get_all_categories()
    
    text = "📂 **Task Categories**\n\n"
    
    for cat in categories:
        status = "✅" if cat['is_active'] else "❌"
        text += f"{status} {cat['name']}\n"
    
    text += f"\nTotal: {len(categories)} categories"
    
    keyboard = [
        [InlineKeyboardButton("➕ Add Category", callback_data="add_category")],
        [InlineKeyboardButton("🔙 Back", callback_data="back_to_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def admin_referrals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    referrals = db.get_all_referrals()
    
    text = "📊 **All Referrals**\n\n"
    text += f"Total Referrals: {len(referrals)}\n"
    text += f"Total Bonuses Paid: ₹{sum(float(r['bonus_amount']) for r in referrals):,.2f}\n\n"
    
    text += "**Recent Referrals:**\n"
    for ref in referrals[:10]:
        referrer_name = ref.get('users', {}).get('name', 'Unknown') if ref.get('users') else 'Unknown'
        status = "✅" if ref['status'] == 'rewarded' else "⏳"
        
        text += (
            f"{status} {referrer_name}\n"
            f"   Bonus: ₹{ref['bonus_amount']}\n"
            f"   Date: {utils.format_date(ref['created_at'])}\n\n"
        )
    
    keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="back_to_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def admin_approve_proofs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    assignments = db.get_all_task_assignments()
    pending_assignments = [a for a in assignments if a['status'] == 'submitted']
    
    if not pending_assignments:
        await query.edit_message_text(
            "✔️ **Task Proofs**\n\n"
            "No pending submissions!",
            parse_mode='Markdown'
        )
        return
    
    text = "✔️ **Pending Task Submissions**\n\n"
    keyboard = []
    
    for assignment in pending_assignments[:10]:
        task_title = assignment.get('tasks', {}).get('title', 'Unknown') if assignment.get('tasks') else 'Unknown'
        task_reward = assignment.get('tasks', {}).get('reward', 0) if assignment.get('tasks') else 0
        taker_name = assignment.get('users', {}).get('name', 'Unknown') if assignment.get('users') else 'Unknown'
        
        text += (
            f"**{task_title}**\n"
            f"Worker: {taker_name}\n"
            f"Reward: ₹{task_reward}\n"
            f"Submitted: {utils.format_date(assignment['submitted_at']) if assignment.get('submitted_at') else 'N/A'}\n"
            f"Doc: {'✅' if assignment.get('proof_file_url') else '❌'} | Video: {'✅' if assignment.get('proof_video_url') else '❌'}\n\n"
        )
        
        keyboard.append([
            InlineKeyboardButton(f"✅ Approve {taker_name[:15]}", callback_data=f"approve_proof_{assignment['id']}"),
            InlineKeyboardButton(f"❌ Reject {taker_name[:15]}", callback_data=f"reject_proof_{assignment['id']}")
        ])
    
    keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="back_to_menu")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def approve_proof(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    assignment_id = query.data.replace('approve_proof_', '')
    
    assignments = db.get_all_task_assignments()
    assignment_data = next((a for a in assignments if a['id'] == assignment_id), None)
    
    result = db.approve_task_submission(assignment_id)
    
    if result and assignment_data:
        task_title = assignment_data.get('tasks', {}).get('title', 'Task')
        task_reward = assignment_data.get('tasks', {}).get('reward', 0)
        taker_telegram_uid = assignment_data.get('users', {}).get('telegram_uid')
        
        try:
            if taker_telegram_uid:
                await context.bot.send_message(
                    chat_id=taker_telegram_uid,
                    text=f"🎉 **Task Approved!**\n\n"
                         f"Your submission for task **{task_title}** has been approved!\n\n"
                         f"💰 Payment of ₹{task_reward} has been added to your wallet.\n\n"
                         f"Keep up the great work!",
                    parse_mode='Markdown'
                )
        except Exception as e:
            print(f"Error sending approval notification to taker: {e}")
        
        await query.edit_message_text(
            "✅ **Task Approved!**\n\n"
            "Worker has been paid and notified.",
            parse_mode='Markdown'
        )
    else:
        await query.edit_message_text(
            "❌ Error approving task.",
            parse_mode='Markdown'
        )

async def reject_proof_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    assignment_id = query.data.replace('reject_proof_', '')
    context.user_data['reject_assignment_id'] = assignment_id
    
    await query.edit_message_text(
        "❌ **Reject Task Submission**\n\n"
        "Please enter the reason for rejection:",
        parse_mode='Markdown'
    )
    return ADMIN_REJECT_PROOF

async def reject_proof_reason(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reason = update.message.text
    assignment_id = context.user_data['reject_assignment_id']
    
    assignments = db.get_all_task_assignments()
    assignment_data = next((a for a in assignments if a['id'] == assignment_id), None)
    
    result = db.reject_task_submission(assignment_id, reason)
    
    if result and assignment_data:
        task_title = assignment_data.get('tasks', {}).get('title', 'Task')
        taker_telegram_uid = assignment_data.get('users', {}).get('telegram_uid')
        
        try:
            if taker_telegram_uid:
                await context.bot.send_message(
                    chat_id=taker_telegram_uid,
                    text=f"❌ **Task Rejected**\n\n"
                         f"Your submission for task **{task_title}** has been rejected.\n\n"
                         f"**Reason:** {reason}\n\n"
                         f"Please review the requirements and resubmit if possible.",
                    parse_mode='Markdown'
                )
        except Exception as e:
            print(f"Error sending rejection notification to taker: {e}")
        
        await update.message.reply_text(
            "❌ **Task Rejected!**\n\n"
            "Worker has been notified.",
            parse_mode='Markdown'
        )
    else:
        await update.message.reply_text(
            "❌ Error rejecting task.",
            parse_mode='Markdown'
        )
    
    context.user_data.clear()
    return ConversationHandler.END
