from sqlalchemy import select, func
from SQL.models import *
from SQL.products.schemas import *
from SQL.base_dao import *
from SQL.database import get_session



class ProductsDAO(BaseDAO):
    model = ProductModel

    async def search_products(query: str):
        async with get_session() as session:
            ts_query = func.to_tsquery("russian", " & ".join(query.split()))
            stmt = select(ProductModel).where(
                func.to_tsvector("russian", ProductModel.name).op("@@")(ts_query)
            )
            result = await session.execute(stmt)
            return result.scalars().all()

    # async def create_product(session: AsyncSession, product: ProductCreate):
    #     session = ProductModel(name=product.name, calories=product.calories)
    #     session.add(db_product)    
    #     await session.commit()
    #     await session.refresh(db_product)
    #     return db_product

    async def get_products():
        async with get_session() as session:
            stmt = select(ProductModel).limit(20)
            result = await session.execute(stmt)
            result_dto = [ProductResponse.model_validate(row, from_attributes=True) for row in result.scalars().all()]
            # [ProductResponse(id=row[0], name=row[1], energy_kcal=row[2]) for row in result]
            return result_dto
        
