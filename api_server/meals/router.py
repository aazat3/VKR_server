from fastapi import APIRouter, Depends, HTTPException, status, Response, Request, Cookie
from fastapi.security import OAuth2PasswordBearer

# from pathlib import Path
import logging

from api_server.user_auth.auth import get_current_user


from SQL.models import *
from SQL.meals.schemas import *
from SQL.meals.dao import *

router = APIRouter(prefix='/meal', tags=['Meal'])

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Эндпоинт для добавления продукта
@router.post("/", response_model=MealResponse)
async def create_meal(meal: MealCreate):
    result = await MealsDAO.add(**meal.model_dump())
    return MealResponse.model_validate(result)

# Эндпоинт для получения всех продуктов
@router.get("/", response_model=list[MealResponse])
async def get_meals():
    result = await MealsDAO.get_meals()
    return result

@router.get("/me/")
async def get_me(user_data: UserModel = Depends(get_current_user)):
# async def get_me(token: str = Depends(oauth2_scheme)):
#     user_data: UserModel = get_current_user(token)
    return user_data