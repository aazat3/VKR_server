from pydantic import BaseModel, EmailStr, Field, field_validator
import re
from datetime import datetime


class MealBase(BaseModel):
    userID: int = Field(..., description="ID пользователя")
    productID: int = Field(..., description="ID продукта")
    weight: int = Field(..., description="Вес продукта")
    time: datetime 

class MealCreate(MealBase):
    pass

class MealResponse(MealBase):
    id: int = Field(..., description="ID приема")

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
