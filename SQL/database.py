import asyncio

from sqlalchemy import String, create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import os

# Данные для подключения
database_url = os.getenv('DATABASE_URL')
database_url_async = os.getenv('DATABASE_URL_async')

DATABASE_URL = database_url
DATABASE_URL_async = database_url_async

# Создание движка SQLAlchemy
engine = create_engine(DATABASE_URL)
engine_async = create_async_engine(DATABASE_URL_async)


# Создание сессии для работы с БД
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
SessionLocal_async = async_sessionmaker(autocommit=False, autoflush=False, bind=engine_async)

# Базовый класс для моделей
# Base = declarative_base()
class Base(DeclarativeBase):
    pass

# Функция для получения сессии (Dependency Injection в FastAPI)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()