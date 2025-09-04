import os

TELEGRAM_TOKEN = "7790027827:AAFdUzmw3Jrvb3R5lcHvfGTxPXamnAvaXzg"

SQL_SERVER_CONNECTION = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=YourServerName;"
    "DATABASE=PatrimonioDB;"
    "UID=YourUser;"
    "PWD=YourPassword"
)

DATA_FOLDER = "data"
EXCEL_FILE_NAME = "patrimonio_report.xlsx"
EXCEL_PATH = os.path.join(DATA_FOLDER, EXCEL_FILE_NAME)