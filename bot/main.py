from telegram.ext import Application, CommandHandler, ConversationHandler, MessageHandler, filters, CallbackQueryHandler
from config import TELEGRAM_TOKEN
from bot.handlers import (
    cancel,
    add_start, add_user,
)

from bot.handlers import (
    ajuda, # <-- Adicione esta linha
    cancel,
)

from bot.handlers import (
    add_start, add_user, add_department, add_type, add_patrimony, add_equipment, add_serial,
    add_invoice, add_purchase_date, add_warranty_end, add_status, add_obs,
    search,
    export,
    update_start, update_select_field, update_new_value,
    remove_start, remover_confirm,
    ADD_USER, ADD_DEPT, ADD_TYPE, ADD_PATRIMONY, ADD_EQUIPMENT, ADD_SERIAL,
    ADD_INVOICE, ADD_PURCHASE_DATE, ADD_WARRANTY_END, ADD_STATUS, ADD_OBS,
    UPDATE_SELECT_FIELD, UPDATE_NEW_VALUE,
    REMOVE_CONFIRMATION,
    unlink_user_start
)

def main():
    """Inicia o bot."""
    app = Application.builder().token(TELEGRAM_TOKEN).build()


    add_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('add', add_start)],
        states={
            ADD_USER: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_user)],
            ADD_DEPT: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_department)],
            ADD_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_type)],
            ADD_PATRIMONY: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_patrimony)],
            ADD_EQUIPMENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_equipment)],
            ADD_SERIAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_serial)],
            ADD_INVOICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_invoice)],
            ADD_PURCHASE_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_purchase_date)],
            ADD_WARRANTY_END: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_warranty_end)],
            ADD_STATUS: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_status)],
            ADD_OBS: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_obs)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        per_user=True
    )


    update_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('update', update_start)],
        states={
            UPDATE_NEW_VALUE: [MessageHandler(filters.TEXT & ~filters.COMMAND, update_new_value)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        per_user=True
    )


    remove_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('remove', remove_start)],
        states={
            REMOVE_CONFIRMATION: [CallbackQueryHandler(remover_confirm)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        per_user=True
    )


    app.add_handler(add_conv_handler)
    app.add_handler(update_conv_handler)
    app.add_handler(remove_conv_handler)

    app.add_handler(CallbackQueryHandler(update_select_field))
    app.add_handler(CallbackQueryHandler(remover_confirm))

    app.add_handler(CommandHandler('ajuda', ajuda))
    app.add_handler(CommandHandler('search', search))
    app.add_handler(CommandHandler('export', export))
    app.add_handler(CommandHandler('unlink_user', unlink_user_start))

    print("Bot iniciado...")
    app.run_polling()


if __name__ == "__main__":
    main()