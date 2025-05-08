from fastapi import APIRouter, Depends, Query
from fastapi.security import OAuth2PasswordBearer
import logging

from user_auth.auth import get_current_user
from SQL.models import *
from SQL.categories.schemas import *
from SQL.categories.dao import *

router = APIRouter(prefix='/category', tags=['category'])

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Эндпоинт для добавления продукта
# @router.post("/", response_model=MealResponse)
# async def create_meal(meal: MealAdd, user_data: UserModel = Depends(get_current_user)):
#     meal = MealCreate(userID=user_data.id, **meal.model_dump())
#     result = await MealsDAO.add(**meal.model_dump())
#     return MealResponse.model_validate(result)

# Эндпоинт для получения всех продуктов
@router.get("/", response_model=list[CategoryResponse])
async def get_meals():
    result = await CategoriesDAO.find_all()
    return result
