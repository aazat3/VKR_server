from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column
from SQL.database import Base, int_pk, str_uniq
from typing import Annotated, Optional
import datetime


time = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int_pk]
    name: Mapped[str_uniq]
    categoryID: Mapped[int] = mapped_column(ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    calories: Mapped[int] = mapped_column(nullable=False)
    proteins: Mapped[int] = mapped_column(nullable=False)
    fats: Mapped[int] = mapped_column(nullable=False)
    carbohydrates: Mapped[int] = mapped_column(nullable=False)
    



class Meal(Base):
    __tablename__ = "meals"

    id: Mapped[int_pk]
    userID: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    productID: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    weight: Mapped[int] = mapped_column(nullable=False)
    time: Mapped[time]


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int_pk]
    name: Mapped[str_uniq]


class User(Base):
    __tablename__ = "users"

    id: Mapped[int_pk]
    name: Mapped[str] = mapped_column(nullable=False)
    login: Mapped[str_uniq]
    password: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str_uniq]


class Device(Base):
    __tablename__ = "devices"

    id: Mapped[int_pk]
    userID: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    serialNumber: Mapped[int] = mapped_column(nullable=False, unique=True,)
