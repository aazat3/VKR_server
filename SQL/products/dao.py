from sqlalchemy import select, func, desc, case
from SQL.models import *
from SQL.products.schemas import *
from SQL.base_dao import *
from SQL.database import async_session_factory



class ProductsDAO(BaseDAO):
    model = ProductModel

    async def search_products_by_name(query: str, limit: int = 20):
        try:
            async with async_session_factory() as session:
                ts_vector = func.to_tsvector('russian', ProductModel.name)
                ts_query = func.plainto_tsquery('russian', query)
                rank = func.ts_rank(ts_vector, ts_query)

                # Выше приоритет, если точное совпадение
                exact_match = case(
                    (func.lower(ProductModel.name) == query.lower(), 1),
                    else_=0
                )

                stmt = (
                    select(ProductModel, rank.label("rank"))
                    .where(ts_vector.op('@@')(ts_query))
                    .order_by(desc(exact_match), desc(rank))  # сначала точные, потом по релевантности
                    .limit(limit)
                )

                result = await session.execute(stmt)
                return [row[0] for row in result.all()]
        except SQLAlchemyError as e:
            print(f"Ошибка при поиске: {e}")
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
        
