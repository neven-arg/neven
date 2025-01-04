from typing import List, Optional
from fastapi import APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from app.database import engine
from app.financings.models import Financing
from app.financings.schemas import FinancingData

router = APIRouter(prefix="/financings", tags=["financings"])


@router.get("", response_model=List[FinancingData])
async def get_financings(bank_id: Optional[int] = None):
    with Session(engine) as db:
        query = db.query(Financing)
        if bank_id:
            query = query.filter(Financing.bank_id == bank_id)
        financings = query.all()
        return financings


@router.get("/{financing_id}", response_model=FinancingData)
async def get_financing(financing_id: int):
    with Session(engine) as db:
        financing = db.query(Financing).filter(Financing.id == financing_id).first()
        if not financing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Financing not found"
            )
        return financing


@router.post("", response_model=FinancingData, status_code=status.HTTP_201_CREATED)
async def create_financing(financing_data: FinancingData):
    with Session(engine) as db:
        db_financing = Financing(**financing_data.model_dump())
        db.add(db_financing)
        db.commit()
        db.refresh(db_financing)
        return db_financing


@router.put("/{financing_id}", response_model=FinancingData)
async def update_financing(financing_id: int, financing_data: FinancingData):
    with Session(engine) as db:
        db_financing = db.query(Financing).filter(Financing.id == financing_id).first()
        if not db_financing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Financing not found"
            )
        db_financing.bank_id = financing_data.bank_id
        db_financing.installments = financing_data.installments
        db_financing.bank_percentage = financing_data.bank_percentage
        db_financing.with_iva = financing_data.with_iva
        db.commit()
        db.refresh(db_financing)
        return db_financing


@router.delete("/{financing_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_financing(financing_id: int):
    with Session(engine) as db:
        financing = db.query(Financing).filter(Financing.id == financing_id).first()
        if not financing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Financing not found"
            )
        db.delete(financing)
        db.commit()
