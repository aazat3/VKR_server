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
            async with session.begin():
                new_instance = cls.model(**values)
                session.add(new_instance)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return new_instance
            

#  @classmethod
#     async def add(cls, **values) -> T:
#         async with async_session_factory() as session:
#             async with session.begin():
#                 instance = cls.model(**values)
#                 session.add(instance)
#                 try:
#                     await session.commit()
#                     await session.refresh(instance)
#                 except SQLAlchemyError as e:
#                     await session.rollback()
#                     raise e
#                 return instance

#     @classmethod
#     async def get_by_id(cls, id_: int) -> T | None:
#         async with async_session_factory() as session:
#             stmt = select(cls.model).where(cls.model.id == id_)
#             result = await session.execute(stmt)
#             return result.scalar_one_or_none()

#     @classmethod
#     async def get_all(cls) -> list[T]:
#         async with async_session_factory() as session:
#             stmt = select(cls.model)
#             result = await session.execute(stmt)
#             return result.scalars().all()

#     @classmethod
#     async def update(cls, id_: int, **values) -> T | None:
#         async with async_session_factory() as session:
#             async with session.begin():
#                 stmt = (
#                     sqlalchemy_update(cls.model)
#                     .where(cls.model.id == id_)
#                     .values(**values)
#                     .returning(cls.model)
#                 )
#                 try:
#                     result = await session.execute(stmt)
#                     await session.commit()
#                     return result.scalar_one_or_none()
#                 except SQLAlchemyError as e:
#                     await session.rollback()
#                     raise e

#     @classmethod
#     async def delete(cls, id_: int) -> bool:
#         async with async_session_factory() as session:
#             async with session.begin():
#                 stmt = sqlalchemy_delete(cls.model).where(cls.model.id == id_)
#                 try:
#                     await session.execute(stmt)
#                     await session.commit()
#                     return True
#                 except SQLAlchemyError:
#                     await session.rollback()
#                     return False