from telegram import Update, InputFile, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler, CommandHandler, MessageHandler, filters, \
    CallbackQueryHandler
from core.services import (
    add_new_asset, get_asset_info, update_asset_field, delete_asset,
    unlink_user_from_asset, get_all_assets_for_export
)
from core.utils import format_asset_details, format_asset_list, format_date_input
from bot.keyboards import get_update_asset_keyboard, get_remove_confirmation_keyboard
from repository.excel_manager import export_to_excel
import os


ADD_USER, ADD_DEPT, ADD_TYPE, ADD_PATRIMONY, ADD_EQUIPMENT, ADD_SERIAL, ADD_INVOICE, ADD_PURCHASE_DATE, ADD_WARRANTY_END, ADD_STATUS, ADD_OBS = range(
    11)


UPDATE_SELECT_FIELD, UPDATE_NEW_VALUE = range(11, 13)


REMOVE_CONFIRMATION = range(13, 14)


# --- Add Asset Handlers ---
async def add_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Vamos cadastrar um novo patrimônio.\nDigite o NOME DO USUÁRIO:")
    return ADD_USER


async def add_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['user'] = update.message.text
    await update.message.reply_text("Digite o DEPARTAMENTO:")
    return ADD_DEPT


async def add_department(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['department'] = update.message.text
    await update.message.reply_text("Digite o TIPO do equipamento (Notebook, Monitor, Celular etc):")
    return ADD_TYPE


async def add_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['type'] = update.message.text
    await update.message.reply_text("Digite o NÚMERO DE PATRIMÔNIO:")
    return ADD_PATRIMONY


async def add_patrimony(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['patrimony_number'] = update.message.text
    await update.message.reply_text("Digite o NOME DO EQUIPAMENTO (modelo/identificação):")
    return ADD_EQUIPMENT


async def add_equipment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['equipment'] = update.message.text
    await update.message.reply_text("Digite o NÚMERO DE SÉRIE (opcional):")
    return ADD_SERIAL


async def add_serial(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['serial_number'] = update.message.text or None
    await update.message.reply_text("Digite o NÚMERO DA NOTA FISCAL (opcional):")
    return ADD_INVOICE


async def add_invoice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['invoice_number'] = update.message.text or None
    await update.message.reply_text("Digite a DATA DE COMPRA (YYYY-MM-DD) (opcional):")
    return ADD_PURCHASE_DATE


async def add_purchase_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text:
        date_obj = format_date_input(text)
        if date_obj is None:
            await update.message.reply_text("Formato de data inválido. Use YYYY-MM-DD.")
            return ADD_PURCHASE_DATE
        context.user_data['purchase_date'] = date_obj
    else:
        context.user_data['purchase_date'] = None
    await update.message.reply_text("Digite a GARANTIA ATÉ (YYYY-MM-DD) (opcional):")
    return ADD_WARRANTY_END


async def add_warranty_end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text:
        date_obj = format_date_input(text)
        if date_obj is None:
            await update.message.reply_text("Formato de data inválido. Use YYYY-MM-DD.")
            return ADD_WARRANTY_END
        context.user_data['warranty_end_date'] = date_obj
    else:
        context.user_data['warranty_end_date'] = None
    await update.message.reply_text("Digite o STATUS do equipamento (opcional):")
    return ADD_STATUS


async def add_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['status'] = update.message.text or None
    await update.message.reply_text("Digite OBSERVAÇÕES (opcional):")
    return ADD_OBS


async def add_obs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['observations'] = update.message.text or None

    if add_new_asset(context.user_data):
        await update.message.reply_text("✅ Patrimônio cadastrado com sucesso!")
    else:
        await update.message.reply_text("❌ Ocorreu um erro ao cadastrar o patrimônio.")

    return ConversationHandler.END



async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if not args:
        await update.message.reply_text(
            "Por favor, use o comando com o número de patrimônio ou o nome do usuário.\nExemplo: /search 804 ou /search João Silva")
        return

    query_term = " ".join(args)
    results = get_asset_info(query_term)

    if query_term.isdigit():
        if results:
            await update.message.reply_text(format_asset_details(results))
        else:
            await update.message.reply_text(f"🚫 Patrimônio com o número **{query_term}** não encontrado.")
    else:
        if not results:
            await update.message.reply_text(f"🚫 Nenhum patrimônio encontrado para o usuário **{query_term}**.")
            return

        message = f"🔎 **Patrimônios encontrados para '{query_term}'**:\n\n"
        for asset in results:
            message += format_asset_list(asset)
            message += "---\n"
        await update.message.reply_text(message)



async def export(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text("⏳ Gerando planilha, por favor aguarde...")
        assets = get_all_assets_for_export()
        if not assets:
            await update.message.reply_text("🚫 Não há patrimônios registrados para exportar.")
            return
        export_to_excel(assets)
        file_path = os.path.join("data", "patrimonio_report.xlsx")
        with open(file_path, 'rb') as f:
            await context.bot.send_document(chat_id=update.effective_chat.id, document=f)
        await update.message.reply_text("✅ Planilha exportada com sucesso!")
    except Exception as e:
        print(f"Erro ao exportar planilha: {e}")
        await update.message.reply_text(
            "❌ Ocorreu um erro ao exportar a planilha. Por favor, tente novamente mais tarde.")



async def update_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if not args:
        await update.message.reply_text(
            "Por favor, use o comando com o número do patrimônio que deseja atualizar.\nExemplo: /update 804")
        return ConversationHandler.END
    patrimony_number = " ".join(args)
    asset = get_asset_info(patrimony_number)
    if not asset:
        await update.message.reply_text(f"🚫 Patrimônio com o número **{patrimony_number}** não encontrado.")
        return ConversationHandler.END
    context.user_data['patrimony_to_update'] = patrimony_number
    await update.message.reply_text(
        f"✅ Patrimônio **{patrimony_number}** encontrado. Qual campo você deseja atualizar?",
        reply_markup=get_update_asset_keyboard()
    )
    return UPDATE_SELECT_FIELD


async def update_select_field(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    field = query.data
    if field == "cancel":
        await query.edit_message_text("❌ Atualização cancelada.")
        return ConversationHandler.END
    context.user_data['field_to_update'] = field
    await query.edit_message_text(f"Por favor, digite o novo valor para o campo '{field}'.")
    return UPDATE_NEW_VALUE


async def update_new_value(update: Update, context: ContextTypes.DEFAULT_TYPE):
    patrimony_number = context.user_data['patrimony_to_update']
    field = context.user_data['field_to_update']
    new_value = update.message.text
    if field in ['purchase_date', 'warranty_end_date']:
        new_value = format_date_input(new_value)
        if new_value is None:
            await update.message.reply_text("Formato de data inválido. Use YYYY-MM-DD.")
            return UPDATE_NEW_VALUE
    if update_asset_field(patrimony_number, field, new_value):
        await update.message.reply_text(
            f"✅ Campo **'{field}'** do patrimônio **{patrimony_number}** atualizado com sucesso!")
    else:
        await update.message.reply_text(f"❌ Ocorreu um erro ao atualizar o patrimônio.")
    context.user_data.clear()
    return ConversationHandler.END



async def remove_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if not args:
        await update.message.reply_text(
            "Por favor, use o comando com o número de patrimônio que deseja remover.\nExemplo: /remove 804")
        return ConversationHandler.END
    patrimony_to_remove = " ".join(args)
    asset = get_asset_info(patrimony_to_remove)
    if not asset:
        await update.message.reply_text(f"🚫 Patrimônio com o número **{patrimony_to_remove}** não encontrado.")
        return ConversationHandler.END
    context.user_data['patrimony_to_remove'] = patrimony_to_remove
    await update.message.reply_text(
        f"⚠️ **ATENÇÃO:** Você tem certeza que deseja remover o patrimônio **{patrimony_to_remove}**?\n"
        f"Esta ação não pode ser desfeita.",
        reply_markup=get_remove_confirmation_keyboard()
    )
    return REMOVE_CONFIRMATION


async def remover_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    patrimony_to_remove = context.user_data.get('patrimony_to_remove')
    if query.data == "confirm_removal":
        if delete_asset(patrimony_to_remove):
            await query.edit_message_text(f"✅ Patrimônio **{patrimony_to_remove}** removido com sucesso!")
        else:
            await query.edit_message_text(f"❌ Ocorreu um erro ao remover o patrimônio.")
    else:
        await query.edit_message_text("❌ Remoção cancelada.")
    context.user_data.clear()
    return ConversationHandler.END



async def unlink_user_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if not args:
        await update.message.reply_text(
            "Por favor, use o comando com o número de patrimônio para desvincular.\nExemplo: /unlink_user 804")
        return
    patrimony_number = " ".join(args)
    if unlink_user_from_asset(patrimony_number):
        await update.message.reply_text(f"✅ Usuário desvinculado do patrimônio **{patrimony_number}** com sucesso!")
    else:
        await update.message.reply_text(f"❌ Patrimônio com o número **{patrimony_number}** não encontrado.")
from telegram.ext import Application, CommandHandler, ConversationHandler, MessageHandler, filters, CallbackQueryHandler
from config import TELEGRAM_TOKEN
from bot.handlers import (
    add_start, add_user, add_department, add_type, add_patrimony, add_equipment, add_serial,
    add_invoice, add_purchase_date, add_warranty_end, add_status, add_obs,
    search,
    export,
    update_start, update_select_field, update_new_value,
    remove_start, remover_confirm, unlink_user_start,
    ADD_USER, ADD_DEPT, ADD_TYPE, ADD_PATRIMONY, ADD_EQUIPMENT, ADD_SERIAL,
    ADD_INVOICE, ADD_PURCHASE_DATE, ADD_WARRANTY_END, ADD_STATUS, ADD_OBS,
    UPDATE_SELECT_FIELD, UPDATE_NEW_VALUE,
    REMOVE_CONFIRMATION
)


def main():
    """Starts the bot."""
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
        fallbacks=[]
    )


    update_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('update', update_start)],
        states={
            UPDATE_SELECT_FIELD: [CallbackQueryHandler(update_select_field)],
            UPDATE_NEW_VALUE: [MessageHandler(filters.TEXT & ~filters.COMMAND, update_new_value)]
        },
        fallbacks=[]
    )


    remove_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('remove', remove_start)],
        states={
            REMOVE_CONFIRMATION: [CallbackQueryHandler(remover_confirm)],
        },
        fallbacks=[]
    )


    app.add_handler(add_conv_handler)
    app.add_handler(update_conv_handler)
    app.add_handler(remove_conv_handler)
    app.add_handler(CommandHandler('search', search))
    app.add_handler(CommandHandler('export', export))
    app.add_handler(CommandHandler('unlink_user', unlink_user_start))

    app.run_polling()


if __name__ == "__main__":
    main()