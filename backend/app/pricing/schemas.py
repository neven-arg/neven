from pydantic import BaseModel


class InputData(BaseModel):
    product_id: int
    financing_id: int
    desired_margin: float = 0.20
