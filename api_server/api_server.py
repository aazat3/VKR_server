from fastapi import FastAPI, Depends, HTTPException, status, Response, Request, Cookie
from fastapi.security import OAuth2PasswordBearer
import uvicorn
from jose import jwt, JWTError
import logging

from SQL.models import *
from SQL.products.schemas import *
from SQL.users.schemas import *
from SQL.base_dao import *
from SQL.users.dao import *
from SQL.products.dao import *
from user_auth.router import router as router_user_auth

from datetime import datetime, timezone

app = FastAPI(
    title="VKR",
    root_path="/api"
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# # Эндпоинт для добавления продукта
# @app.post("/products/", response_model=ProductResponse)
# def create_product(product: ProductCreate, db: AsyncSession = Depends(get_session)):
#     return ProductsDAO.create_product(db, product)

# Эндпоинт для получения всех продуктов
@app.get("/products/", response_model=list[ProductResponse])
async def products():
    return await ProductsDAO.get_products()


app.include_router(router_user_auth)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
