from fastapi import APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from app.database import engine
from app.financings.models import Financing
from app.products.models import Product
from app.pricing.schemas import InputData
from app.pricing.utils import calculate_final_percentage, calculate_selling_price

router = APIRouter(prefix="/pricing", tags=["pricing"])


@router.post("/calculate_price")
async def calculate_price(product_input: InputData):
    with Session(engine) as db:
        product = (
            db.query(Product).filter(Product.id == product_input.product_id).first()
        )
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
            )

        financing = (
            db.query(Financing)
            .filter(Financing.id == product_input.financing_id)
            .first()
        )
        if not financing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Financing not found"
            )

        final_percentage = calculate_final_percentage(
            financing.bank_percentage, financing.iva, financing.with_iva  # type: ignore
        )
        selling_price = calculate_selling_price(
            product.acquisition_cost, product_input.desired_margin, final_percentage  # type: ignore
        )

        if selling_price == -1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The financing percentage is not compatible with the desired margin.",
            )

        return {
            "selling_price": round(selling_price, 2),
        }
