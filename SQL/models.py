from sqlalchemy import Column, Integer, String, Float
from SQL.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    calories = Column(Float, nullable=False)