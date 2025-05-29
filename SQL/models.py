from sqlalchemy import ForeignKey, text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from SQL.database import Base, int_pk, str_uniq
from typing import Annotated, Optional
from datetime import datetime


time = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]


class ProductModel(Base):
    __tablename__ = "products"

    id: Mapped[int_pk]
    categoryID: Mapped[int] = mapped_column(ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)    # код
    name: Mapped[str]
    source_type_id: Mapped[int] = mapped_column(default=1, nullable=False)
    added_by_user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True
    )
    energy_kcal: Mapped[int] = mapped_column(nullable=True)                # Ккал
    water_percent: Mapped[int] = mapped_column(nullable=True)              # вода
    protein_percent: Mapped[int] = mapped_column(nullable=True)            # бел
    fat_percent: Mapped[int] = mapped_column(nullable=True)                # жир
    carbohydrates_percent: Mapped[int] = mapped_column(nullable=True)      # угл (всего углеводов)
    
    saturatedfa_percent: Mapped[int] = mapped_column(nullable=True)        # нжк (насыщенные жирные кислоты)
    cholesterol_mg: Mapped[int] = mapped_column(nullable=True)             # хол
    monodisaccharides_percen: Mapped[int] = mapped_column(nullable=True)   # мдс
    starch_percent: Mapped[int] = mapped_column(nullable=True)             # кр
    fiber_percent: Mapped[int] = mapped_column(nullable=True)              # пв
    organicacids_percent: Mapped[int] = mapped_column(nullable=True)       # ок
    ash_percent: Mapped[int] = mapped_column(nullable=True)                # зола
    sodium_mg: Mapped[int] = mapped_column(nullable=True)                  # na
    potassium_mg: Mapped[int] = mapped_column(nullable=True)               # k
    calcium_mg: Mapped[int] = mapped_column(nullable=True)                 # ca
    magnesium_mg: Mapped[int] = mapped_column(nullable=True)               # mg
    phosphorus_mg: Mapped[int] = mapped_column(nullable=True)              # p
    iron_mg: Mapped[int] = mapped_column(nullable=True)                    # fe
    retinol_ug: Mapped[int] = mapped_column(nullable=True)                 # а
    betacarotene_ug: Mapped[int] = mapped_column(nullable=True)            # кар
    retinoleq_ug: Mapped[int] = mapped_column(nullable=True)               # рэ
    tocopheroleq_mg: Mapped[int] = mapped_column(nullable=True)            # тэ
    thiamine_mg: Mapped[int] = mapped_column(nullable=True)                # b1
    riboflavin_mg: Mapped[int] = mapped_column(nullable=True)              # b2
    niacin_mg: Mapped[int] = mapped_column(nullable=True)                  # рр
    niacineq_mg: Mapped[int] = mapped_column(nullable=True)                # нэ
    ascorbicacid_mg: Mapped[int] = mapped_column(nullable=True)            # с
    polyunsaturatedfa_percent: Mapped[int] = mapped_column(nullable=True)  # ПНЖК
    ethanol_percent: Mapped[int] = mapped_column(nullable=True)            # алк

    category: Mapped["CategoryModel"] = relationship(back_populates="products")
    meals: Mapped[list["MealModel"]] = relationship(back_populates="product")
    user: Mapped["UserModel"] = relationship(back_populates="products")
    

class MealModel(Base):
    __tablename__ = "meals"

    id: Mapped[int_pk]
    userID: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    productID: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    weight: Mapped[int] = mapped_column(nullable=False)
    time: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped["UserModel"] = relationship(back_populates="meals")
    product: Mapped["ProductModel"] = relationship(back_populates="meals")


class CategoryModel(Base):
    __tablename__ = "categories"

    id: Mapped[int_pk]
    name: Mapped[str_uniq]

    products: Mapped[list["ProductModel"]] = relationship(back_populates="category")


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int_pk]
    name: Mapped[str] = mapped_column(nullable=False)
    login: Mapped[str_uniq]
    password: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str_uniq]

    meals: Mapped[list["MealModel"]] = relationship(back_populates="user")
    product: Mapped["ProductModel"] = relationship(back_populates="users")
    device: Mapped[list["DeviceModel"]] = relationship(back_populates="user")


class DeviceModel(Base):
    __tablename__ = "devices"

    id: Mapped[int_pk]
    userID: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    serialNumber: Mapped[int] = mapped_column(nullable=False, unique=True,)
    
    user: Mapped["UserModel"] = relationship(back_populates="device")


