# models/asset.py

from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class Asset:
    user: str
    department: str
    type: str
    patrimony_number: str
    equipment: str
    serial_number: Optional[str] = None
    invoice_number: Optional[str] = None
    purchase_date: Optional[date] = None
    warranty_end_date: Optional[date] = None
    status: Optional[str] = None
    observations: Optional[str] = None