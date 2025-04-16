from datetime import datetime
from typing import Annotated
from sqlalchemy import String, func
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from SQL.config import settings

DATABASE_URL_asyncpg = settings.DATABASE_URL_asyncpg
async_engine  = create_async_engine(DATABASE_URL_asyncpg)
async_session_factory  = async_sessionmaker(autocommit=False, autoflush=False, bind=async_engine)


# настройка аннотаций
int_pk = Annotated[int, mapped_column(primary_key=True, index=True)]
created_at = Annotated[datetime, mapped_column(server_default=func.now())]
updated_at = Annotated[datetime, mapped_column(server_default=func.now(), onupdate=datetime.now)]
str_uniq = Annotated[str, mapped_column(unique=True, nullable=False)]
str_null_true = Annotated[str, mapped_column(nullable=True)]
str_256 = Annotated[str, 256]


class Base(DeclarativeBase):
    type_annotation_map = {
        str_256: String(256)
    }

    repr_cols_num = 3
    repr_cols = tuple()
    
    def __repr__(self):
        """Relationships не используются в repr(), т.к. могут вести к неожиданным подгрузкам"""
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"

# Функция для получения сессии (Dependency Injection в FastAPI)
async def get_session():
    async with async_session_factory() as session:
        yield session