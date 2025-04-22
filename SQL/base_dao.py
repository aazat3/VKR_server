from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from SQL.database import async_session_factory


class BaseDAO:
    model = None
    
    @classmethod
    async def find_all(cls):
        async with async_session_factory() as session:
            query = select(cls.model)
            result = await session.execute(query)
            return result.scalars().all()
    
    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_factory() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()
    
    @classmethod
    async def find_one_or_none_by_id(cls, data_id: int):
        async with async_session_factory() as session:
            query = select(cls.model).filter_by(id=data_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()
    
    @classmethod
    async def add(cls, **values): 
        async with async_session_factory() as session:
            new_instance = cls.model(**values)
            session.add(new_instance)
            try:
                await session.flush()
                await session.refresh(new_instance)
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                raise e
            return new_instance
