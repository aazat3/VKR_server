from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Данные для подключения
DATABASE_URL = "postgresql://admin:admin@host.docker.internal:5432/nutrition_db"

# Создание движка SQLAlchemy
engine = create_engine(DATABASE_URL)

# Создание сессии для работы с БД
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей
Base = declarative_base()

# Функция для получения сессии (Dependency Injection в FastAPI)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()