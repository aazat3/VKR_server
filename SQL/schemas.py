from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    calories: float

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int

    class Config:
        from_attributes = True  # Позволяет SQLAlchemy объектам преобразовываться в Pydantic
        orm_mode = True
