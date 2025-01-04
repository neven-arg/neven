from sqlalchemy import Column, Integer, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.database import Base


class Financing(Base):
    __tablename__ = "financings"
    id = Column(Integer, primary_key=True, index=True)
    bank_id = Column(Integer, ForeignKey("banks.id"))
    installments = Column(Integer)
    bank_percentage = Column(Float)
    iva = Column(Float, default=0.21)
    with_iva = Column(Boolean, default=False)
    bank = relationship("Bank", back_populates="financings")
