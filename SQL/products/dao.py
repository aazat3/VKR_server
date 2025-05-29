from sqlalchemy import select, func, desc, case
from sqlalchemy.orm import aliased, contains_eager, joinedload, selectinload
import logging

from SQL.models import *
from SQL.products.schemas import *
from SQL.base_dao import *
from SQL.database import async_session_factory

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ProductsDAO(BaseDAO):
    model = ProductModel

    async def get_products_by_name(query: str, limit: int = 20):
        try:
            async with async_session_factory() as session:
                ts_vector = func.to_tsvector("russian", ProductModel.name)
                ts_query = func.plainto_tsquery("russian", query)
                rank = func.ts_rank(ts_vector, ts_query)

                # 1. Точное совпадение (приоритет 3)
                exact_match = case(
                    (func.lower(ProductModel.name) == query.lower(), 3),
                    (
                        ProductModel.name.ilike(f"%{query}%"),
                        2,
                    ),  # частичное совпадение (приоритет 2)
                    else_=1,  # остальные (приоритет 1)
                )

                # 2. Длина имени (короткие выше)
                name_length = func.length(ProductModel.name)

                stmt = (
                    select(ProductModel, rank.label("rank"))
                    .where(ts_vector.op("@@")(ts_query))
                    .options(joinedload(ProductModel.category))
                    .order_by(desc(exact_match), name_length, desc(rank))
                    .limit(limit)
                )

                result = await session.execute(stmt)
                return [row[0] for row in result.all()]
        except Exception as e:
            print(f"Ошибка при поиске: {e}")
            return []

    async def add_product(
        **optional_fields,  # Остальные необязательные параметры
    ) -> ProductModel:
        # Убедитесь, что не передается явный id
        if "id" in optional_fields:
            del optional_fields["id"]  # Удаляем явно переданный id
            logger.info(f"optional_fields have product id")
        try:
            async with async_session_factory() as session:
                async with session.begin():
                    # Создаем объект продукта
                    new_product = ProductModel(**optional_fields)
                    session.add(new_product)
                    await session.flush()
                    await session.refresh(new_product)
                    return new_product
        except SQLAlchemyError as e:
            logger.error(f"Error adding product: {str(e)}")
            raise RuntimeError("Database error occurred")

    async def get_products_simple():
        async with async_session_factory() as session:
            stmt = select(ProductModel).limit(20)
            result = await session.execute(stmt)
            # result_dto = [ProductResponse.model_validate(row, from_attributes=True) for row in result.scalars().all()]
            return result.scalars().all()

    async def get_products(
        size: int = 50,
        after_id: int | None = None,
    ):
        async with async_session_factory() as session:
            stmt = select(ProductModel)
            if after_id:
                stmt = stmt.filter(ProductModel.id > after_id)

            stmt = (
                stmt.options(joinedload(ProductModel.category))
                .order_by(ProductModel.id.asc())
                .limit(size)
            )
            result = await session.execute(stmt)
            return result.scalars().all()

    async def get_products_by_user(
        user_id: int,
        size: int = 50,
        after_id: int | None = None,
    ):
        async with async_session_factory() as session:
            stmt = select(ProductModel)
            if after_id:
                stmt = stmt.filter(ProductModel.id > after_id)
            stmt = stmt.filter(ProductModel.added_by_user_id == user_id)
            stmt = (
                stmt.options(joinedload(ProductModel.category))
                .order_by(ProductModel.id.asc())
                .limit(size)
            )
            result = await session.execute(stmt)
            return result.scalars().all()
