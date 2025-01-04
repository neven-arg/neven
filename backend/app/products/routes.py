from typing import List
from fastapi import APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from app.database import engine
from app.products.models import Product
from app.products.schemas import ProductData

router = APIRouter(prefix="/products", tags=["products"])


@router.post("", response_model=ProductData, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductData):
    with Session(engine) as db:
        reception_cost = product.purchase_price * 0.05
        acquisition_cost = product.purchase_price + reception_cost
        db_product = Product(
            **product.model_dump(exclude={"reception_cost", "acquisition_cost"}),
            reception_cost=reception_cost,
            acquisition_cost=acquisition_cost,
        )
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product


@router.get("", response_model=List[ProductData])
async def get_products():
    with Session(engine) as db:
        products = db.query(Product).all()
        return products


@router.get("/{product_id}", response_model=ProductData)
async def get_product(product_id: int):
    with Session(engine) as db:
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
            )
        return product


@router.put("/{product_id}", response_model=ProductData)
async def update_product(product_id: int, product: ProductData):
    with Session(engine) as db:
        db_product = db.query(Product).filter(Product.id == product_id).first()
        if not db_product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
            )
        reception_cost = product.purchase_price * 0.05
        acquisition_cost = product.purchase_price + reception_cost
        db_product.name = product.name
        db_product.purchase_price = product.purchase_price
        db_product.reception_cost = reception_cost
        db_product.acquisition_cost = acquisition_cost
        db.commit()
        db.refresh(db_product)
        return db_product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int):
    with Session(engine) as db:
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
            )
        db.delete(product)
        db.commit()
