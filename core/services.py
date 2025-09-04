# core/services.py

from repository.db_manager import DBManager
from models.asset import Asset
from datetime import datetime

db = DBManager()
db.create_table()

def add_new_asset(asset_data: dict) -> bool:
    """Adds a new asset to the database."""
    try:
        new_asset = Asset(
            user=asset_data['user'],
            department=asset_data['department'],
            type=asset_data['type'],
            patrimony_number=asset_data['patrimony_number'],
            equipment=asset_data['equipment'],
            serial_number=asset_data.get('serial_number'),
            invoice_number=asset_data.get('invoice_number'),
            purchase_date=asset_data.get('purchase_date'),
            warranty_end_date=asset_data.get('warranty_end_date'),
            status=asset_data.get('status'),
            observations=asset_data.get('observations')
        )
        db.add_asset(new_asset)
        return True
    except Exception as e:
        print(f"Error adding asset: {e}")
        return False

def get_asset_info(query: str):
    """Retrieves asset information based on patrimony number or user name."""
    if query.isdigit():
        return db.get_asset_by_patrimony_number(query)
    else:
        return db.get_assets_by_user(query)

def update_asset_field(patrimony_number: str, field: str, new_value):
    """Updates a single field of an asset."""
    return db.update_asset(patrimony_number, field, new_value)

def unlink_user_from_asset(patrimony_number: str):
    """Unlinks a user from an asset by setting the 'user' field to None."""
    return db.update_asset(patrimony_number, 'user', None)

def delete_asset(patrimony_number: str):
    """Deletes an asset from the database."""
    return db.delete_asset(patrimony_number)

def get_all_assets_for_export():
    """Retrieves all assets for the purpose of exporting."""
    return db.get_all_assets()