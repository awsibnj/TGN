from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
import database as db
import config
import utils
import asyncio

DEPOSIT_AMOUNT, DEPOSIT_METHOD, DEPOSIT_UTR = range(3)
WITHDRAW_METHOD, WITHDRAW_DETAILS, WITHDRAW_AMOUNT = range(3)

async def wallet_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user = update.effective_user
    existing_user = db.get_user_by_telegram_uid(user.id)
    
    balance = existing_user.get('wallet_balance', 0)
    transactions = db.get_wallet_transactions(existing_user['id'])
    
    recent_txns = transactions[:5]
    txn_text = ""
    for txn in recent_txns:
        status_emoji = {'pending': '⏳', 'approved': '✅', 'rejected': '❌'}.get(txn['status'], '❓')
        type_emoji = {
            'deposit': '💵',
            'withdrawal': '💸',
            'task_payment': '💰',
            'referral_bonus': '🎁',
            'task_deduction': '📤'
        }.get(txn['transaction_type'], '💳')
        
        amount_str = f"+₹{txn['amount']}" if txn['transaction_type'] in ['deposit', 'task_payment', 'referral_bonus'] else f"-₹{txn['amount']}"
        txn_text += f"{status_emoji} {type_emoji} {amount_str} - {utils.format_date(txn['created_at'])}\n"
    
    text = (
        f"💰 **Wallet**\n\n"
        f"Balance: **₹{float(balance):,.2f}**\n\n"
        f"**Recent Transactions:**\n{txn_text if txn_text else 'No transactions yet.'}\n"
    )
    
    keyboard = [
        [InlineKeyboardButton("💵 Add Balance", callback_data="wallet_add_balance")],
        [InlineKeyboardButton("💸 Withdraw", callback_data="wallet_withdraw")],
        [InlineKeyboardButton("📊 All Transactions", callback_data="wallet_all_transactions")],
        [InlineKeyboardButton("🔙 Back", callback_data="back_to_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def add_balance_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        f"💵 **Add Balance**\n\n"
        f"Enter the amount you want to add (₹{config.MIN_DEPOSIT} - ₹{config.MAX_DEPOSIT}):",
        parse_mode='Markdown'
    )
    return DEPOSIT_AMOUNT

async def deposit_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        amount = float(update.message.text)
        if amount < config.MIN_DEPOSIT or amount > config.MAX_DEPOSIT:
            raise ValueError
        context.user_data['deposit_amount'] = amount
    except:
        await update.message.reply_text(
            f"❌ Invalid amount. Please enter between ₹{config.MIN_DEPOSIT} and ₹{config.MAX_DEPOSIT}:",
            parse_mode='Markdown'
        )
        return DEPOSIT_AMOUNT
    
    keyboard = [
        [InlineKeyboardButton("UPI", callback_data="deposit_upi")],
        [InlineKeyboardButton("Crypto", callback_data="deposit_crypto")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "💳 **Select Payment Method:**",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
    return DEPOSIT_METHOD

async def deposit_method(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    method = query.data.replace('deposit_', '')
    context.user_data['deposit_method'] = method
    
    payment_info = db.get_payment_info(method)
    
    if not payment_info:
        await query.edit_message_text(
            "❌ Payment method not available. Please contact support.",
            parse_mode='Markdown'
        )
        return ConversationHandler.END
    
    details = payment_info['details']
    
    if method == 'upi':
        upi_id = details.get('upi_id', 'N/A')
        text = (
            f"💳 **UPI Payment**\n\n"
            f"Amount: ₹{context.user_data['deposit_amount']}\n\n"
            f"UPI ID: `{upi_id}`\n\n"
            f"Please complete the payment and wait for 2 minutes.\n"
            f"Then you'll be able to submit your UTR/Transaction ID."
        )
        
        qr_url = details.get('qr_code_url')
        if qr_url:
            await query.edit_message_text(text, parse_mode='Markdown')
        else:
            qr_image = utils.generate_qr_code(upi_id)
            await context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=qr_image,
                caption=text,
                parse_mode='Markdown'
            )
    else:
        wallet_address = details.get('wallet_address', 'N/A')
        network = details.get('network', 'USDT-TRC20')
        text = (
            f"💰 **Crypto Payment**\n\n"
            f"Amount: ₹{context.user_data['deposit_amount']}\n\n"
            f"Network: {network}\n"
            f"Wallet Address: `{wallet_address}`\n\n"
            f"Please complete the payment and wait for 2 minutes.\n"
            f"Then you'll be able to submit your Transaction ID."
        )
        await query.edit_message_text(text, parse_mode='Markdown')
    
    await asyncio.sleep(config.PAYMENT_VERIFICATION_DELAY)
    
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="⏰ **Time's up!**\n\nPlease enter your **UTR/Transaction ID**:",
        parse_mode='Markdown'
    )
    
    return DEPOSIT_UTR

async def deposit_utr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    utr = update.message.text
    context.user_data['deposit_utr'] = utr
    
    user = update.effective_user
    existing_user = db.get_user_by_telegram_uid(user.id)
    
    payment_details = {
        'method': context.user_data['deposit_method'],
        'utr': utr
    }
    
    transaction = db.create_wallet_transaction(
        existing_user['id'],
        'deposit',
        context.user_data['deposit_amount'],
        payment_method=context.user_data['deposit_method'],
        payment_details=payment_details,
        utr_transaction_id=utr
    )
    
    if transaction:
        await update.message.reply_text(
            "✅ **Deposit Request Submitted!**\n\n"
            f"Amount: ₹{context.user_data['deposit_amount']}\n"
            f"UTR: {utr}\n\n"
            "Your request is pending admin approval.\n"
            "You'll be notified once approved.",
            parse_mode='Markdown'
        )
    else:
        await update.message.reply_text(
            "❌ Error submitting request. Please try again or contact support.",
            parse_mode='Markdown'
        )
    
    context.user_data.clear()
    return ConversationHandler.END

async def withdraw_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user = update.effective_user
    existing_user = db.get_user_by_telegram_uid(user.id)
    balance = float(existing_user.get('wallet_balance', 0))
    
    if balance < config.MIN_WITHDRAWAL:
        await query.edit_message_text(
            f"❌ **Insufficient Balance**\n\n"
            f"Minimum withdrawal: ₹{config.MIN_WITHDRAWAL}\n"
            f"Your balance: ₹{balance:,.2f}",
            parse_mode='Markdown'
        )
        return ConversationHandler.END
    
    keyboard = [
        [InlineKeyboardButton("UPI", callback_data="withdraw_upi")],
        [InlineKeyboardButton("Bank Transfer", callback_data="withdraw_bank")],
        [InlineKeyboardButton("Crypto", callback_data="withdraw_crypto")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        f"💸 **Withdraw Funds**\n\n"
        f"Available Balance: ₹{balance:,.2f}\n"
        f"Minimum: ₹{config.MIN_WITHDRAWAL}\n\n"
        f"Select withdrawal method:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
    return WITHDRAW_METHOD

async def withdraw_method(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    method = query.data.replace('withdraw_', '')
    context.user_data['withdraw_method'] = method
    
    if method == 'upi':
        prompt = "Enter your **UPI ID**:"
    elif method == 'bank':
        prompt = "Enter your **Bank Account Details** (Account No, IFSC, Name):"
    else:
        prompt = "Enter your **Crypto Wallet Address** (with network):"
    
    await query.edit_message_text(prompt, parse_mode='Markdown')
    return WITHDRAW_DETAILS

async def withdraw_details(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['withdraw_details'] = update.message.text
    
    user = update.effective_user
    existing_user = db.get_user_by_telegram_uid(user.id)
    balance = float(existing_user.get('wallet_balance', 0))
    
    await update.message.reply_text(
        f"💰 Enter **withdrawal amount** (Max: ₹{balance:,.2f}):",
        parse_mode='Markdown'
    )
    return WITHDRAW_AMOUNT

async def withdraw_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    existing_user = db.get_user_by_telegram_uid(user.id)
    balance = float(existing_user.get('wallet_balance', 0))
    
    try:
        amount = float(update.message.text)
        if amount < config.MIN_WITHDRAWAL:
            raise ValueError(f"Minimum withdrawal is ₹{config.MIN_WITHDRAWAL}")
        if amount > balance:
            raise ValueError(f"Insufficient balance")
        context.user_data['withdraw_amount'] = amount
    except ValueError as e:
        await update.message.reply_text(
            f"❌ Invalid amount. {str(e)}\n\nPlease try again:",
            parse_mode='Markdown'
        )
        return WITHDRAW_AMOUNT
    
    payment_details = {
        'method': context.user_data['withdraw_method'],
        'details': context.user_data['withdraw_details']
    }
    
    db.update_wallet_balance(existing_user['id'], -amount)
    
    transaction = db.create_wallet_transaction(
        existing_user['id'],
        'withdrawal',
        amount,
        payment_method=context.user_data['withdraw_method'],
        payment_details=payment_details
    )
    
    if transaction:
        await update.message.reply_text(
            "✅ **Withdrawal Request Submitted!**\n\n"
            f"Amount: ₹{amount}\n"
            f"Method: {context.user_data['withdraw_method'].upper()}\n\n"
            "Your request is pending admin approval.\n"
            "Funds will be transferred once approved.",
            parse_mode='Markdown'
        )
    else:
        db.update_wallet_balance(existing_user['id'], amount)
        await update.message.reply_text(
            "❌ Error submitting withdrawal. Please try again or contact support.",
            parse_mode='Markdown'
        )
    
    context.user_data.clear()
    return ConversationHandler.END

async def all_transactions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user = update.effective_user
    existing_user = db.get_user_by_telegram_uid(user.id)
    
    transactions = db.get_wallet_transactions(existing_user['id'])
    
    if not transactions:
        await query.edit_message_text(
            "📊 **All Transactions**\n\n"
            "No transactions yet.",
            parse_mode='Markdown'
        )
        return
    
    text = "📊 **All Transactions**\n\n"
    
    for txn in transactions[:20]:
        status_emoji = {'pending': '⏳', 'approved': '✅', 'rejected': '❌'}.get(txn['status'], '❓')
        type_emoji = {
            'deposit': '💵',
            'withdrawal': '💸',
            'task_payment': '💰',
            'referral_bonus': '🎁',
            'task_deduction': '📤'
        }.get(txn['transaction_type'], '💳')
        
        amount_str = f"+₹{txn['amount']}" if txn['transaction_type'] in ['deposit', 'task_payment', 'referral_bonus'] else f"-₹{txn['amount']}"
        
        text += (
            f"{status_emoji} {type_emoji} {amount_str}\n"
            f"   Type: {txn['transaction_type'].replace('_', ' ').title()}\n"
            f"   Date: {utils.format_date(txn['created_at'])}\n\n"
        )
    
    await query.edit_message_text(text, parse_mode='Markdown')

async def cancel_wallet_operation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        "❌ Operation cancelled. Use /start to access your dashboard.",
        parse_mode='Markdown'
    )
    return ConversationHandler.END
