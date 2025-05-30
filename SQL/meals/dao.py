from sqlalchemy import select, func
from sqlalchemy.orm import aliased, contains_eager, joinedload, selectinload
from datetime import date, timedelta

from SQL.models import *
from SQL.meals.schemas import *
from SQL.base_dao import *
from SQL.database import async_session_factory



class MealsDAO(BaseDAO):
    model = MealModel

    # async def search_products_by_name(query: str):
    #     async with async_session_factory() as session:
    #         ts_query = func.to_tsquery("russian", " & ".join(query.split()))
    #         stmt = select(ProductModel).where(
    #             func.to_tsvector("russian", ProductModel.name).op("@@")(ts_query)
    #         )
    #         result = await session.execute(stmt)
    #         return result.scalars().all()

    # async def add_meal(meal: MealCreate):
    #     async with async_session_factory() as session:
    #         new_instance = MealModel()
    #         session.add(new_instance)    
    #         await session.commit()
    #         await session.refresh()
    #         return new_instance

    async def delete_meal(meal_id: int, user_id: int) -> MealModel:
        async with async_session_factory() as session:
            # Получаем прием пищи с проверкой владельца
            stmt = select(MealModel).where(
                (MealModel.id == meal_id) & 
                (MealModel.userID == user_id)
            )
            
            result = await session.execute(stmt)
            meal = result.scalar_one_or_none()
            
            if not meal:
                raise 
            if meal.userID != user_id:
                raise 
            
            # Удаляем запись
            await session.delete(meal)
            await session.commit()
            
            return meal
            
    async def get_meals(
            userID,    
            size: int = 50,
            after_id: int | None = None, 
            start_date: datetime | None = None, 
            end_date: datetime | None = None) -> list[ProductModel]:
        async with async_session_factory() as session:
            stmt = select(MealModel).where(MealModel.userID == userID)
            
            if start_date or end_date:
                if start_date:
                    # Конвертируем datetime в date с вызовом метода ()
                    stmt = stmt.where(MealModel.time >= start_date.date())
                if end_date:
                    # Добавляем время 23:59:59 к конечной дате
                    end_date_with_time = end_date.replace(hour=23, minute=59, second=59)
                    stmt = stmt.where(MealModel.time <= end_date_with_time)

                # Если указана конечная дата, но не указана начальная
                if end_date and not start_date:
                    # Берем период 24 часа до конечной даты
                    start_date = end_date - timedelta(days=1)
                    stmt = stmt.where(MealModel.time >= start_date)
            
            if after_id:
                stmt = stmt.filter(MealModel.id > after_id)

            stmt = stmt.options(joinedload(MealModel.product).joinedload(ProductModel.category)).order_by(MealModel.id.desc()).limit(size) 
            result = await session.execute(stmt)
            return result.scalars().all()
            
