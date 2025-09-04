
import os

TELEGRAM_TOKEN = "TOKEN_TELEGRAM"

SQL_SERVER_CONNECTION = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=seu_servidor.database.windows.net;"  
    "DATABASE=seu_banco_de_dados;"              
    "UID=usuario_bd;"                  
    "PWD=senha_db"
)

DATA_FOLDER = "data"
EXCEL_FILE_NAME = "patrimonio_report.xlsx"
EXCEL_PATH = os.path.join(DATA_FOLDER, EXCEL_FILE_NAME)