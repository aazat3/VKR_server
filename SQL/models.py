from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import Mapped, mapped_column
from SQL.database import Base

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column( primary_key=True, index=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    calories: Mapped[int] = mapped_column(nullable=False)

    # id = Column(Integer, primary_key=True, index=True)
    # name = Column(String, unique=True, nullable=False)
    # calories = Column(Float, nullable=False)