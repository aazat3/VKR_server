from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from SQL.database import Base, int_pk, str_uniq
from typing import Annotated, Optional
import datetime


time = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]


class ProductModel(Base):
    __tablename__ = "products"

    id: Mapped[int_pk]
    name: Mapped[str_uniq]
    categoryID: Mapped[int] = mapped_column(ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    calories: Mapped[int] = mapped_column(nullable=False)
    proteins: Mapped[int] = mapped_column(nullable=False)
    fats: Mapped[int] = mapped_column(nullable=False)
    carbohydrates: Mapped[int] = mapped_column(nullable=False)

    category: Mapped["CategoryModel"] = relationship(back_populates="products")
    meals: Mapped[list["MealModel"]] = relationship(back_populates="products")

    

class MealModel(Base):
    __tablename__ = "meals"

    id: Mapped[int_pk]
    userID: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    productID: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    weight: Mapped[int] = mapped_column(nullable=False)
    time: Mapped[time]

    user: Mapped["UserModel"] = relationship(back_populates="meals")
    product: Mapped["ProductModel"] = relationship(back_populates="meals")


class CategoryModel(Base):
    __tablename__ = "categories"

    id: Mapped[int_pk]
    name: Mapped[str_uniq]

    products: Mapped[list["ProductModel"]] = relationship(back_populates="categories")


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int_pk]
    name: Mapped[str] = mapped_column(nullable=False)
    login: Mapped[str_uniq]
    password: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str_uniq]

    meals: Mapped[list["MealModel"]] = relationship(back_populates="users")
    devices: Mapped[list["DeviceModel"]] = relationship(back_populates="users")


class DeviceModel(Base):
    __tablename__ = "devices"

    id: Mapped[int_pk]
    userID: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    serialNumber: Mapped[int] = mapped_column(nullable=False, unique=True,)
    
    user: Mapped["UserModel"] = relationship(back_populates="devices")


