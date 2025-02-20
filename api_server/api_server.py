import random
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pathlib import Path
import logging
from ..database import database, models, schemas, crud


app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



# @app.get("/weights")
# def get_data():
#     db_path = Path(__file__).parent.parent / 'database'  / 'weights.db'
#     conn = sqlite3.connect(db_path.resolve())
#     cursor = conn.cursor()
#     cursor.execute("SELECT device_id, weight, timestamp FROM weight_data ORDER BY timestamp DESC LIMIT 10")
#     data = cursor.fetchall()
#     conn.close()

#     return [{"device_id": row[0], "weight": row[1], "timestamp": row[2]} for row in data]

# Эндпоинт для добавления продукта
@app.post("/products/", response_model=schemas.ProductResponse)
def create_product(product: schemas.ProductCreate, db: Session = Depends(database.get_db)):
    return crud.create_product(db, product)

# Эндпоинт для получения всех продуктов
@app.get("/products/", response_model=list[schemas.ProductResponse])
def get_products(db: Session = Depends(database.get_db)):
    return crud.get_products(db)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        # "http://localhost:5173",
        # "http://31.129.43.117",
        "http://aazatserver.ru",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
