from typing import List
from fastapi import APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.database import engine
from app.banks.models import Bank
from app.banks.schemas import BankData

router = APIRouter(prefix="/banks", tags=["banks"])


@router.post("", response_model=BankData, status_code=status.HTTP_201_CREATED)
async def create_bank(bank: BankData):
    with Session(engine) as db:
        try:
            db_bank = Bank(**bank.model_dump())
            db.add(db_bank)
            db.commit()
            db.refresh(db_bank)
            return db_bank
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nombre de banco ya existe, por favor elige otro",
            )


@router.get("", response_model=List[BankData])
async def get_banks():
    with Session(engine) as db:
        banks = db.query(Bank).all()
        return banks


@router.get("/{bank_id}", response_model=BankData)
async def get_bank(bank_id: int):
    with Session(engine) as db:
        bank = db.query(Bank).filter(Bank.id == bank_id).first()
        if not bank:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Banco no encontrado"
            )
        return bank


@router.put("/{bank_id}", response_model=BankData)
async def update_bank(bank_id: int, bank: BankData):
    with Session(engine) as db:
        db_bank = db.query(Bank).filter(Bank.id == bank_id).first()
        if not db_bank:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Banco no encontrado"
            )
        db_bank.name = bank.name
        try:
            db.commit()
            db.refresh(db_bank)
            return db_bank
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nombre de banco ya existe, por favor elige otro",
            )


@router.delete("/{bank_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_bank(bank_id: int):
    with Session(engine) as db:
        bank = db.query(Bank).filter(Bank.id == bank_id).first()
        if not bank:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Banco no encontrado"
            )
        db.delete(bank)
        db.commit()
