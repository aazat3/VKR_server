from sqlalchemy import select, func
from SQL.models import *
from SQL.products.schemas import *
from SQL.base_dao import *
from SQL.database import async_session_factory



class ProductsDAO(BaseDAO):
    model = ProductModel

    async def search_products_by_name(query: str, limit: int = 10):
        try:
            async with async_session_factory() as session:
                # Разбиваем запрос по словам и формируем ts_query
                query = query.lower().strip()
                ts_query = func.to_tsquery("russian", " & ".join(query.split()))
                tsvector = func.to_tsvector("russian", ProductModel.name)
                rank = func.ts_rank(tsvector, ts_query)

                stmt = (
                    select(ProductModel)
                    .where(tsvector.op("@@")(ts_query))
                    .order_by((rank).desc)  # сортировка по релевантности
                    .limit(limit)
                )

                result = await session.execute(stmt)
                return result.scalars().all()
        except SQLAlchemyError as e:
            print(f"Ошибка при поиске продуктов: {e}")
            return []

    # async def create_product(session: AsyncSession, product: ProductCreate):
    #     session = ProductModel(name=product.name, calories=product.calories)
    #     session.add(db_product)    
    #     await session.commit()
    #     await session.refresh(db_product)
    #     return db_product

    async def get_products():
        async with async_session_factory() as session:
            stmt = select(ProductModel).limit(20)
            result = await session.execute(stmt)
            # result_dto = [ProductResponse.model_validate(row, from_attributes=True) for row in result.scalars().all()]
            return result.scalars().all()
        
