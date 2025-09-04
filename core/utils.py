from datetime import date, datetime

def format_asset_details(asset_data: tuple) -> str:
    """Formata os detalhes de um único patrimônio para exibição."""

    return (
        f"**Detalhes do Patrimônio:**\n"
        f"Usuário: {asset_data[1] or 'N/A'}\n"
        f"Departamento: {asset_data[2] or 'N/A'}\n"
        f"Tipo: {asset_data[3] or 'N/A'}\n"
        f"Patrimônio: {asset_data[4] or 'N/A'}\n"
        f"Equipamento: {asset_data[5] or 'N/A'}\n"
        f"Nº de Série: {asset_data[6] or 'N/A'}\n"
        f"Nota Fiscal: {asset_data[7] or 'N/A'}\n"
        f"Data de Compra: {asset_data[8].strftime('%d/%m/%Y') if asset_data[8] else 'N/A'}\n"
        f"Garantia Até: {asset_data[9].strftime('%d/%m/%Y') if asset_data[9] else 'N/A'}\n"
        f"Status: {asset_data[10] or 'N/A'}\n"
        f"Observações: {asset_data[11] or 'N/A'}"
    )

def format_asset_list(asset_data: tuple) -> str:
    """Formata um resumo de patrimônio para exibição em lista."""
    return (
        f"Patrimônio: **{asset_data[4]}**\n"
        f"Equipamento: {asset_data[5]}\n"
        f"Usuário: {asset_data[1]}\n"
        f"Departamento: {asset_data[2]}\n"
    )

def format_date_input(date_text: str) -> date | None:
    """Converte uma string de data (YYYY-MM-DD) para um objeto date."""
    if date_text:
        try:
            return datetime.strptime(date_text, "%Y-%m-%d").date()
        except ValueError:
            return None
    return None