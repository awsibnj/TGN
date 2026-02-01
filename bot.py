import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    filters,
)
import config
from handlers import start, provider, taker, wallet, admin, support

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def back_to_menu(update: Update, context):
    query = update.callback_query
    await query.answer()
    
    user = update.effective_user
    import database as db
    existing_user = db.get_user_by_telegram_uid(user.id)
    
    if existing_user:
        await start.show_main_menu(update, context, existing_user)

def main():
    application = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start.start))
    
    application.add_handler(CallbackQueryHandler(start.verify_join, pattern="^verify_join$"))
    application.add_handler(CallbackQueryHandler(start.read_terms, pattern="^read_terms$"))
    application.add_handler(CallbackQueryHandler(start.back_to_start, pattern="^back_to_start$"))
    application.add_handler(CallbackQueryHandler(back_to_menu, pattern="^back_to_menu$"))
    
    provider_registration_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(provider.register_provider_start, pattern="^register_provider$")],
        states={
            provider.PROVIDER_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, provider.provider_name)],
            provider.PROVIDER_MOBILE: [MessageHandler(filters.TEXT & ~filters.COMMAND, provider.provider_mobile)],
            provider.PROVIDER_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, provider.provider_email)],
            provider.PROVIDER_GENDER: [CallbackQueryHandler(provider.provider_gender, pattern="^gender_")],
            provider.PROVIDER_DOB: [MessageHandler(filters.TEXT & ~filters.COMMAND, provider.provider_dob)],
            provider.PROVIDER_LOCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, provider.provider_location)],
            provider.PROVIDER_PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, provider.provider_password)],
            provider.PROVIDER_CONFIRM_PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, provider.provider_confirm_password)],
            provider.PROVIDER_REFERRAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, provider.provider_referral)],
        },
        fallbacks=[CommandHandler("cancel", provider.cancel_registration)],
    )
    application.add_handler(provider_registration_conv)
    
    taker_registration_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(taker.register_taker_start, pattern="^register_taker$")],
        states={
            taker.TAKER_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, taker.taker_name)],
            taker.TAKER_MOBILE: [MessageHandler(filters.TEXT & ~filters.COMMAND, taker.taker_mobile)],
            taker.TAKER_DOB: [MessageHandler(filters.TEXT & ~filters.COMMAND, taker.taker_dob)],
            taker.TAKER_PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, taker.taker_password)],
            taker.TAKER_CONFIRM_PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, taker.taker_confirm_password)],
            taker.TAKER_REFERRAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, taker.taker_referral)],
        },
        fallbacks=[CommandHandler("cancel", taker.cancel_taker_registration)],
    )
    application.add_handler(taker_registration_conv)
    
    create_task_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(provider.create_task_start, pattern="^provider_create_task$")],
        states={
            provider.TASK_TITLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, provider.task_title)],
            provider.TASK_DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, provider.task_description)],
            provider.TASK_CATEGORY: [CallbackQueryHandler(provider.task_category, pattern="^cat_")],
            provider.TASK_REWARD: [MessageHandler(filters.TEXT & ~filters.COMMAND, provider.task_reward)],
            provider.TASK_SLOTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, provider.task_slots)],
            provider.TASK_REQUIREMENTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, provider.task_requirements)],
        },
        fallbacks=[CommandHandler("cancel", provider.cancel_registration)],
    )
    application.add_handler(create_task_conv)
    
    application.add_handler(CallbackQueryHandler(provider.view_provider_tasks, pattern="^provider_view_tasks$"))
    application.add_handler(CallbackQueryHandler(provider.provider_refer, pattern="^provider_refer$"))
    application.add_handler(CallbackQueryHandler(provider.provider_campaign, pattern="^provider_campaign$"))
    application.add_handler(CallbackQueryHandler(provider.provider_lifetime_earn, pattern="^provider_lifetime_earn$"))
    
    application.add_handler(CallbackQueryHandler(taker.get_new_task, pattern="^taker_get_task$"))
    application.add_handler(CallbackQueryHandler(taker.view_tasks, pattern="^view_tasks_"))
    application.add_handler(CallbackQueryHandler(taker.take_task, pattern="^take_task_"))
    application.add_handler(CallbackQueryHandler(taker.my_tasks, pattern="^taker_my_tasks$"))
    application.add_handler(CallbackQueryHandler(taker.taker_refer, pattern="^taker_refer$"))
    
    submit_task_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(taker.submit_task_start, pattern="^submit_task_")],
        states={
            taker.SUBMIT_PROOF_DOC: [
                MessageHandler(filters.Document.ALL | filters.TEXT, taker.submit_proof_document)
            ],
            taker.SUBMIT_PROOF_VIDEO: [
                MessageHandler(filters.VIDEO | filters.TEXT, taker.submit_proof_video)
            ],
        },
        fallbacks=[CommandHandler("cancel", taker.cancel_submission)],
    )
    application.add_handler(submit_task_conv)
    
    application.add_handler(CallbackQueryHandler(wallet.wallet_menu, pattern="^(provider_wallet|taker_wallet)$"))
    application.add_handler(CallbackQueryHandler(wallet.all_transactions, pattern="^wallet_all_transactions$"))
    
    add_balance_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(wallet.add_balance_start, pattern="^wallet_add_balance$")],
        states={
            wallet.DEPOSIT_AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, wallet.deposit_amount)],
            wallet.DEPOSIT_METHOD: [CallbackQueryHandler(wallet.deposit_method, pattern="^deposit_")],
            wallet.DEPOSIT_UTR: [MessageHandler(filters.TEXT & ~filters.COMMAND, wallet.deposit_utr)],
        },
        fallbacks=[CommandHandler("cancel", wallet.cancel_wallet_operation)],
    )
    application.add_handler(add_balance_conv)
    
    withdraw_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(wallet.withdraw_start, pattern="^wallet_withdraw$")],
        states={
            wallet.WITHDRAW_METHOD: [CallbackQueryHandler(wallet.withdraw_method, pattern="^withdraw_")],
            wallet.WITHDRAW_DETAILS: [MessageHandler(filters.TEXT & ~filters.COMMAND, wallet.withdraw_details)],
            wallet.WITHDRAW_AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, wallet.withdraw_amount)],
        },
        fallbacks=[CommandHandler("cancel", wallet.cancel_wallet_operation)],
    )
    application.add_handler(withdraw_conv)
    
    application.add_handler(CallbackQueryHandler(admin.admin_users, pattern="^admin_users$"))
    application.add_handler(CallbackQueryHandler(admin.admin_tasks, pattern="^admin_tasks$"))
    application.add_handler(CallbackQueryHandler(admin.admin_transactions, pattern="^admin_transactions$"))
    application.add_handler(CallbackQueryHandler(admin.approve_transaction, pattern="^approve_txn_"))
    application.add_handler(CallbackQueryHandler(admin.reject_transaction, pattern="^reject_txn_"))
    application.add_handler(CallbackQueryHandler(admin.admin_support, pattern="^admin_support$"))
    application.add_handler(CallbackQueryHandler(admin.admin_payment_info, pattern="^admin_payment_info$"))
    application.add_handler(CallbackQueryHandler(admin.admin_categories, pattern="^admin_categories$"))
    application.add_handler(CallbackQueryHandler(admin.admin_referrals, pattern="^admin_referrals$"))
    application.add_handler(CallbackQueryHandler(admin.admin_approve_proofs, pattern="^admin_approve_proofs$"))
    application.add_handler(CallbackQueryHandler(admin.approve_proof, pattern="^approve_proof_"))
    
    reject_proof_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(admin.reject_proof_start, pattern="^reject_proof_")],
        states={
            admin.ADMIN_REJECT_PROOF: [MessageHandler(filters.TEXT & ~filters.COMMAND, admin.reject_proof_reason)],
        },
        fallbacks=[CommandHandler("cancel", wallet.cancel_wallet_operation)],
    )
    application.add_handler(reject_proof_conv)
    
    support_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(support.support_start, pattern="^(provider_support|taker_support)$")],
        states={
            support.SUPPORT_MESSAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, support.support_message)],
        },
        fallbacks=[CommandHandler("cancel", support.cancel_support)],
    )
    application.add_handler(support_conv)
    
    logger.info("Bot started successfully!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
