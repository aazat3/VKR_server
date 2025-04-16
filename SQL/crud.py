from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from SQL.models import *
from SQL.schemas import *

async def search_products(query: str, db: AsyncSession):
    ts_query = func.to_tsquery("russian", " & ".join(query.split()))
    stmt = select(ProductModel).where(
        func.to_tsvector("russian", ProductModel.name).op("@@")(ts_query)
    )
    result = await db.execute(stmt)
    return result.scalars().all()

async def create_product(db: AsyncSession, product: ProductCreate):
    db_product = ProductModel(name=product.name, calories=product.calories)
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product

async def get_products(db: AsyncSession):
    stmt = select(ProductModel.id, ProductModel.name, ProductModel.energy_kcal).limit(20)
    result = await db.execute(stmt)
    result_dto = [ProductResponse.model_validate(row, from_attributes=True) for row in result.scalars().all()]
    # [ProductResponse(id=row[0], name=row[1], energy_kcal=row[2]) for row in result]
    return result_dto
    
