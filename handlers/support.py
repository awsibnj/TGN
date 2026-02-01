from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
import database as db

SUPPORT_MESSAGE = 1

async def support_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        "💬 **Support**\n\n"
        "Please describe your issue or question:",
        parse_mode='Markdown'
    )
    return SUPPORT_MESSAGE

async def support_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    user = update.effective_user
    existing_user = db.get_user_by_telegram_uid(user.id)
    
    support_msg = db.create_support_message(existing_user['id'], message)
    
    if support_msg:
        await update.message.reply_text(
            "✅ **Message Sent!**\n\n"
            "Your support request has been submitted.\n"
            "Our team will get back to you soon!",
            parse_mode='Markdown'
        )
    else:
        await update.message.reply_text(
            "❌ Error sending message. Please try again.",
            parse_mode='Markdown'
        )
    
    return ConversationHandler.END

async def cancel_support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "❌ Support request cancelled. Use /start to access your dashboard.",
        parse_mode='Markdown'
    )
    return ConversationHandler.END
