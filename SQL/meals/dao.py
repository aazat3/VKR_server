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

    async def get_meals_simple(userID):
        async with async_session_factory() as session:
            stmt = select(MealModel).where(MealModel.userID == userID).options(joinedload(MealModel.product)).order_by(MealModel.time.desc()) 
            result = await session.execute(stmt)
            # result_dto = [MealResponse.model_validate(row, from_attributes=True) for row in result.scalars().all()]
            return result.scalars().all()
        
    async def get_meals(
            userID,    
            size: int = 50,
            after_id: int | None = None, 
            start_date: datetime | None = None, 
            end_date: datetime | None = None) -> list[ProductModel]:
        async with async_session_factory() as session:
            stmt = select(MealModel).where(MealModel.userID == userID)
            
            if end_date:
                stmt = stmt.where(MealModel.time <= start_date.date)
                if start_date:
                    stmt = stmt.where(MealModel.time >= end_date.date)
                else:
                    stmt = stmt.where(MealModel.time >= start_date.date - timedelta(days=1))
            
            if after_id:
                stmt = stmt.filter(MealModel.id > after_id)

            stmt = stmt.options(joinedload(MealModel.product).joinedload(ProductModel.category)).order_by(MealModel.id.desc()).limit(size) 
            result = await session.execute(stmt)
            return result.scalars().all()
            
