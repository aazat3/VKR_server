from fastapi import APIRouter, Depends, HTTPException, status, Response, Request, Cookie
from fastapi.security import OAuth2PasswordBearer
import uvicorn
from jose import jwt, JWTError


# from pathlib import Path
import logging

from auth import *

from SQL.models import *
from SQL.meals.schemas import *
from SQL.base_dao import *
from SQL.meals.dao import *

router = APIRouter(prefix='/meal', tags=['Meal'])

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Эндпоинт для добавления продукта
@router.post("/", response_model=MealResponse)
async def create_meal(meal: MealCreate):
    result = await MealsDAO.add(**meal.model_dump())
    return result

# Эндпоинт для получения всех продуктов
@router.get("/", response_model=list[MealResponse])
async def get_meals():
    result = await MealsDAO.get_meals()
    return result
