from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator
import re
from SQL.categories.schemas import CategoryResponse


class ProductBase(BaseModel):
    categoryID: int
    name: str
    source_type_id: int = 3  
    energy_kcal: int
    water_percent: Optional[int] = None
    protein_percent: int
    fat_percent: int
    carbohydrates_percent: int
    saturatedfa_percent: Optional[int] = None
    cholesterol_mg: Optional[int] = None
    monodisaccharides_percen: Optional[int] = None
    starch_percent: Optional[int] = None
    fiber_percent: Optional[int] = None
    organicacids_percent: Optional[int] = None
    ash_percent: Optional[int] = None
    sodium_mg: Optional[int] = None
    potassium_mg: Optional[int] = None
    calcium_mg: Optional[int] = None
    magnesium_mg: Optional[int] = None
    phosphorus_mg: Optional[int] = None
    iron_mg: Optional[int] = None
    retinol_ug: Optional[int] = None
    betacarotene_ug: Optional[int] = None
    retinoleq_ug: Optional[int] = None
    tocopheroleq_mg: Optional[int] = None
    thiamine_mg: Optional[int] = None
    riboflavin_mg: Optional[int] = None
    niacin_mg: Optional[int] = None
    niacineq_mg: Optional[int] = None
    ascorbicacid_mg: Optional[int] = None
    polyunsaturatedfa_percent: Optional[int] = None
    ethanol_percent: Optional[int] = None


class ProductAdd(ProductBase):
    pass

class ProductCreate(ProductBase):
    added_by_user_id: Optional[int] = None

class ProductResponse(ProductBase):
    id: int
    added_by_user_id: Optional[int] = None

    class Config:
        from_attributes = True  # Позволяет SQLAlchemy объектам преобразовываться в Pydantic

class ProductResponseWithCategory(ProductResponse):
    category: "CategoryResponse"

    class Config:
        from_attributes = True  # Позволяет SQLAlchemy объектам преобразовываться в Pydantic

    # phone_number: str = Field(..., description="Номер телефона в международном формате, начинающийся с '+'")
    # last_name: str = Field(..., min_length=3, max_length=50, description="Фамилия, от 3 до 50 символов")

    # @field_validator("phone_number")
    # @classmethod
    # def validate_phone_number(cls, value: str) -> str:
    #     if not re.match(r'^\+\d{5,15}$', value):
    #         raise ValueError('Номер телефона должен начинаться с "+" и содержать от 5 до 15 цифр')
    #     return value