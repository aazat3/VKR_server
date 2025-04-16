from sqlalchemy.orm import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from SQL.models import *
from SQL.schemas import *

async def search_products(query: str, db: AsyncSession):
    ts_query = func.to_tsquery("russian", " & ".join(query.split()))
    stmt = select(ProductModel).where(
        func.to_tsvector("russian", ProductModel.name + " " + ProductModel.description).op("@@")(ts_query)
    )
    result = await db.execute(stmt)
    return result.scalars().all()

def create_product(db: AsyncSession, product: ProductCreate):
    db_product = ProductModel(name=product.name, calories=product.calories)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_products(db: AsyncSession):
    return db.query(ProductModel).all()
    
