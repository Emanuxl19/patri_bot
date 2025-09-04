from openpyxl import Workbook
from datetime import date
from config import EXCEL_PATH, DATA_FOLDER
import os


def export_to_excel(data: list):
    """
    Exports a list of asset data to an Excel (.xlsx) file.
    The data should be a list of tuples/objects with columns in the specified order.
    """
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Assets"

    # Headers for the columns
    columns = ["ID", "User", "Department", "Type", "Patrimony Number", "Equipment",
               "Serial Number", "Invoice Number", "Purchase Date", "Warranty End Date", "Status"]
    sheet.append(columns)

    for row in data:
        # The 'Observations' column (index 11) is not exported
        formatted_row = list(row)

        # Convert date objects to a friendly string format
        if formatted_row[8] and isinstance(formatted_row[8], date):
            formatted_row[8] = formatted_row[8].strftime("%Y-%m-%d")
        if formatted_row[9] and isinstance(formatted_row[9], date):
            formatted_row[9] = formatted_row[9].strftime("%Y-%m-%d")

        sheet.append(formatted_row[:11])

    # Ensure the data directory exists
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)

    workbook.save(EXCEL_PATH)
    print(f"Spreadsheet saved at: {EXCEL_PATH}")