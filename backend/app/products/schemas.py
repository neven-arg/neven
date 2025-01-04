from typing import Optional
from pydantic import BaseModel


class ProductData(BaseModel):
    id: Optional[int] = None
    name: str
    purchase_price: float
    reception_cost: Optional[float] = None
    acquisition_cost: Optional[float] = None
