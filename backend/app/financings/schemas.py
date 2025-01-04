from typing import Optional
from pydantic import BaseModel


class FinancingData(BaseModel):
    id: Optional[int] = None
    bank_id: int
    installments: int
    bank_percentage: float
    iva: float = 0.21
    with_iva: bool = True
