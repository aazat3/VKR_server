from fastapi import APIRouter, Depends, Query
from fastapi.security import OAuth2PasswordBearer
import uvicorn
from jose import jwt, JWTError


# from pathlib import Path
import logging

from user_auth.auth import get_current_user

from SQL.models import *
from SQL.products.schemas import *
from SQL.products.dao import *

router = APIRouter(prefix="/product", tags=["Product"])

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Эндпоинт для добавления продукта
@router.post("/", response_model=ProductResponse)
async def add_products(
    product: ProductAdd, user_data: UserModel = Depends(get_current_user)
):
    new_product = ProductCreate(
        added_by_user_id=user_data.id,
        categoryID=product.categoryID,
        name=product.name,
        source_type_id=product.source_type_id,
        energy_kcal=product.energy_kcal,
        protein_percent=product.protein_percent,
        fat_percent=product.fat_percent,
        carbohydrates_percent=product.carbohydrates_percent,
        **product.model_dump(
            exclude={
                "categoryID",
                "name",
                "source_type_id",
                "energy_kcal",
                "protein_percent",
                "fat_percent",
                "carbohydrates_percent",
            }
        )
    )
    result = await ProductsDAO.add_product(new_product)
    return result


# Эндпоинт для получения всех продуктов
@router.get("/", response_model=list[ProductResponseWithCategory])
async def get_products(
    size: int = Query(50, ge=1, le=100),
    after_id: int | None = Query(None, description="Возвращать записи после этого ID"),
):
    return await ProductsDAO.get_products(size, after_id)


# Эндпоинт для получения всех продуктов по названию
@router.get("/search", response_model=list[ProductResponseWithCategory])
async def get_products_by_name(
    size: int = Query(50, ge=1, le=100),
    name: str | None = Query(None, description="Название продукта"),
):
    return await ProductsDAO.get_products_by_name(name, size)
