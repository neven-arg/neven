from sqlalchemy import Column, Integer, Float, String
from app.database import Base


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    purchase_price = Column(Float)
    reception_cost = Column(Float)
    acquisition_cost = Column(Float)
