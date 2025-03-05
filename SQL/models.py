from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from SQL.database import Base
from typing import Annotated, Optional
import datetime


time = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    calories: Mapped[int] = mapped_column(nullable=False)

class Meal(Base):
    __tablename__ = "meals"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("workers.id", ondelete="CASCADE"), unique=True, nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("workers.id", ondelete="CASCADE"),nullable=False)
    weight: Mapped[int] = mapped_column(unique=True, nullable=False)
    time: Mapped[int] = mapped_column(unique=True, nullable=False)


class Product_category(Base):
    __tablename__ = "products_categories"

    id: Mapped[int] = mapped_column( primary_key=True, index=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    calories: Mapped[int] = mapped_column(nullable=False)

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column( primary_key=True, index=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    calories: Mapped[int] = mapped_column(nullable=False)
