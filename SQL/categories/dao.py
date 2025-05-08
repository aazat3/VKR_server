from sqlalchemy import select, func
from sqlalchemy.orm import aliased, contains_eager, joinedload, selectinload
from datetime import date, timedelta

from SQL.models import *
from SQL.categories.schemas import *
from SQL.base_dao import *
from SQL.database import async_session_factory



class CategoriesDAO(BaseDAO):
    model = CategoryModel

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

   
