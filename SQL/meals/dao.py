from sqlalchemy import select, func
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

    async def get_meals(userID):
        async with async_session_factory() as session:
            stmt = select(MealModel).where(MealModel.userID == userID).limit(20)
            result = await session.execute(stmt)
            # result_dto = [MealResponse.model_validate(row, from_attributes=True) for row in result.scalars().all()]
            return result.scalars().all()
        
