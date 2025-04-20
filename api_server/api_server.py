from fastapi import FastAPI, Depends, HTTPException, status
import uvicorn
from sqlalchemy.ext.asyncio import AsyncSession

# from pathlib import Path
import logging

from auth import get_password_hash

from SQL.models import *
from SQL.products.schemas import *
from SQL.users.schemas import *
from SQL.base_dao import *
from SQL.users.dao import *
from SQL.products.dao import *

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# # Эндпоинт для добавления продукта
# @app.post("/products/", response_model=ProductResponse)
# def create_product(product: ProductCreate, db: AsyncSession = Depends(get_session)):
#     return ProductsDAO.create_product(db, product)

# Эндпоинт для получения всех продуктов
@app.get("/products/", response_model=list[ProductResponse])
async def products():
    return await ProductsDAO.get_products()

@app.post("/register/")
async def register_user(user_data: UserRegister) -> dict:
    user = await UsersDAO.find_one_or_none(email=user_data.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пользователь уже существует'
        )
    user_dict = user_data.model_dump()
    user_dict['password'] = get_password_hash(user_data.password)
    await UsersDAO.add(**user_dict)
    return {'message': 'Вы успешно зарегистрированы!'} 


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
