import pyodbc
from config import SQL_SERVER_CONNECTION
from models.asset import Asset
from datetime import datetime


class DBManager:
    def __init__(self):
        """Initializes the DBManager and establishes a database connection."""
        self.conn = None
        self.cursor = None
        self.connect()

    def connect(self):
        """Establishes a connection to the database."""
        try:
            self.conn = pyodbc.connect(SQL_SERVER_CONNECTION)
            self.cursor = self.conn.cursor()
            print("Successfully connected to the database.")
        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            if sqlstate == '28000':
                print("Erro de autenticação: Verifique o nome de usuário e a senha no arquivo config.py")
            else:
                print(f"Erro ao conectar ao banco de dados: {ex}")
            self.conn = None
            self.cursor = None

    def create_table(self):
        """Creates the 'Assets' table if it doesn't exist."""
        if not self.conn:
            return
        self.cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Assets' and xtype='U')
        CREATE TABLE Assets (
            id INT IDENTITY(1,1) PRIMARY KEY,
            [user] NVARCHAR(100),
            department NVARCHAR(100),
            [type] NVARCHAR(50),
            patrimony_number NVARCHAR(50) UNIQUE,
            equipment NVARCHAR(100),
            serial_number NVARCHAR(100),
            invoice_number NVARCHAR(50),
            purchase_date DATE,
            warranty_end_date DATE,
            status NVARCHAR(50),
            observations NVARCHAR(200)
        )
        """)
        self.conn.commit()
        print("Table 'Assets' verified/created.")

    def add_asset(self, asset: Asset):
        """Adds a new asset to the database."""
        if not self.conn:
            return
        self.cursor.execute("""
            INSERT INTO Assets
            ([user], department, [type], patrimony_number, equipment, serial_number,
             invoice_number, purchase_date, warranty_end_date, status, observations)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            asset.user, asset.department, asset.type, asset.patrimony_number, asset.equipment,
            asset.serial_number, asset.invoice_number, asset.purchase_date, asset.warranty_end_date,
            asset.status, asset.observations
        )
        self.conn.commit()

    def get_asset_by_patrimony_number(self, patrimony_number: str):
        """Retrieves a single asset by its patrimony number."""
        if not self.conn:
            return None
        self.cursor.execute("SELECT * FROM Assets WHERE patrimony_number = ?", patrimony_number)
        return self.cursor.fetchone()

    def get_assets_by_user(self, user: str):
        """Retrieves all assets assigned to a specific user (partial match)."""
        if not self.conn:
            return []
        self.cursor.execute("SELECT * FROM Assets WHERE [user] LIKE ?", f"%{user}%")
        return self.cursor.fetchall()

    def get_all_assets(self):
        """Retrieves all assets from the database."""
        if not self.conn:
            return []
        self.cursor.execute("SELECT * FROM Assets")
        return self.cursor.fetchall()

    def update_asset(self, patrimony_number: str, field: str, new_value):
        """Updates a specific field of an asset."""
        if not self.conn:
            return False

        sql_query = f"UPDATE Assets SET [{field}] = ? WHERE patrimony_number = ?"
        self.cursor.execute(sql_query, new_value, patrimony_number)
        self.conn.commit()
        return self.cursor.rowcount > 0

    def delete_asset(self, patrimony_number: str):
        """Deletes an asset from the database by its patrimony number."""
        if not self.conn:
            return False
        self.cursor.execute("DELETE FROM Assets WHERE patrimony_number = ?", patrimony_number)
        self.conn.commit()
        return self.cursor.rowcount > 0
