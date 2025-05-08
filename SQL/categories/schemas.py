from pydantic import BaseModel, EmailStr, Field, field_validator
import re
from datetime import datetime

class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    id: int

    class Config:
        from_attributes = True