import os

TELEGRAM_TOKEN = "7790027827:AAGfOTBs65rp25ERJI0sAH4RJzrUEBJ9-FE"

SQL_SERVER_CONNECTION = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=patribot.database.windows.net;"  
    "DATABASE=Bot_patrimonio;"              
    "UID=Emanuel.martins;"                  
    "PWD=BotTeste2025"
)

DATA_FOLDER = "data"
EXCEL_FILE_NAME = "patrimonio_report.xlsx"
EXCEL_PATH = os.path.join(DATA_FOLDER, EXCEL_FILE_NAME)