from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    energy_kcal: int

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int

    class Config:
        from_attributes = True  # Позволяет SQLAlchemy объектам преобразовываться в Pydantic
