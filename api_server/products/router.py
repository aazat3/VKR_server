from fastapi import APIRouter, Depends, HTTPException, status, Response, Request, Cookie
from fastapi.security import OAuth2PasswordBearer
import uvicorn
from jose import jwt, JWTError


# from pathlib import Path
import logging

from user_auth.auth import get_current_user

from SQL.models import *
from SQL.products.schemas import *
from SQL.products.dao import *

router = APIRouter(prefix='/product', tags=['Product'])

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# # Эндпоинт для добавления продукта
# @app.post("/products/", response_model=ProductResponse)
# def create_product(product: ProductCreate, db: AsyncSession = Depends(get_session)):
#     return ProductsDAO.create_product(db, product)

# Эндпоинт для получения всех продуктов
@router.get("/", response_model=list[ProductResponse])
async def products():
    return await ProductsDAO.get_products()
