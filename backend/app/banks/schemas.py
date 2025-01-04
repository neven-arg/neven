from typing import Optional
from pydantic import BaseModel


class BankData(BaseModel):
    id: Optional[int] = None
    name: str
