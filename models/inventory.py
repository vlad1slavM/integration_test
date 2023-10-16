from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class InventoryModel(BaseModel):
    store_ext_id: str
    price_ext_id: str
    snap_datetime: datetime
    in_matrix: Optional[bool]
    qty: float
    sell_price: Optional[float]
    prime_cost: Optional[float]
    min_stock_level: Optional[float]
    stock_in_days: Optional[int]
    in_transit: Optional[float]
