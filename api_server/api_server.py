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
from products.router import router as router_products
from meals.router import router as router_meals
from categories.router import router as router_categories


from datetime import datetime, timezone

app = FastAPI(
    title="VKR",
    root_path="/api"
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app.include_router(router_user_auth)
app.include_router(router_products)
app.include_router(router_meals)
app.include_router(router_categories)



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
