from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security import OAuth2PasswordBearer
import logging

from user_auth.auth import get_current_user
from SQL.models import *
from SQL.meals.schemas import *
from SQL.meals.dao import *

router = APIRouter(prefix='/meal', tags=['Meal'])

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Эндпоинт для добавления продукта
@router.post("/", response_model=MealResponse)
async def add_meal(meal: MealAdd, user_data: UserModel = Depends(get_current_user)):
    meal = MealCreate(userID=user_data.id, **meal.model_dump())
    result = await MealsDAO.add(**meal.model_dump())
    return MealResponse.model_validate(result)

@router.delete("/", response_model=MealResponse)
async def delete_meal(
    user_data: UserModel = Depends(get_current_user), 
    meal: MealDelete = Query(None, description="Удалить прием с ID"),):

    result = await MealsDAO.delete_meal(meal.id, user_data.id)
    return result

# Эндпоинт для получения всех продуктов
@router.get("/", response_model=list[MealResponseWithProduct])
async def get_meals(
    user_data: UserModel = Depends(get_current_user),
    size: int = Query(50, ge=1, le=100),
    after_id: int | None = Query(None, description="Возвращать записи после этого ID"),
    start_date: datetime = Query(None, description="Начальаня дата для фильтрации", example="2025-04-01T00:00:00"),
    end_date: datetime = Query(None, description="Конечная дата для фильтрации", example="2025-04-30T23:59:59")
    ):
    result = await MealsDAO.get_meals(user_data.id, size, after_id, start_date, end_date)
    return result

@router.get("/me/")
async def get_me(user_data: UserModel = Depends(get_current_user)):
# async def get_me(token: str = Depends(oauth2_scheme)):
#     user_data: UserModel = get_current_user(token)
    return user_data