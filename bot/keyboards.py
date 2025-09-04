from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_update_asset_keyboard():
    """Retorna o teclado inline com opções para atualização de patrimônio."""
    keyboard = [
        [InlineKeyboardButton("Usuário", callback_data="user")],
        [InlineKeyboardButton("Departamento", callback_data="department")],
        [InlineKeyboardButton("Tipo", callback_data="type")],
        [InlineKeyboardButton("Equipamento", callback_data="equipment")],
        [InlineKeyboardButton("Nº de Série", callback_data="serial_number")],
        [InlineKeyboardButton("Nota Fiscal", callback_data="invoice_number")],
        [InlineKeyboardButton("Data Compra", callback_data="purchase_date")],
        [InlineKeyboardButton("Garantia Até", callback_data="warranty_end_date")],
        [InlineKeyboardButton("Status", callback_data="status")],
        [InlineKeyboardButton("Observações", callback_data="observations")],
        [InlineKeyboardButton("Cancelar", callback_data="cancel")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_remove_confirmation_keyboard():
    """Retorna o teclado inline para confirmação de remoção."""
    keyboard = [
        [
            InlineKeyboardButton("Sim, tenho certeza", callback_data="confirm_removal"),
            InlineKeyboardButton("Não, cancelar", callback_data="cancel_removal")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)