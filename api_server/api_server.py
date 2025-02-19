import random
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import sqlite3
from pathlib import Path


app = FastAPI()


@app.get("/weights")
def get_data():
    # items = [
    #     {
    #         "id": 1,
    #         "name": "Docker",
    #         "img": "https://static-00.iconduck.com/assets.00/docker-icon-2048x2048-5mc7mvtn.png",
    #     },
    #     {
    #         "id": 2,
    #         "name": "Nginx",
    #         "img": "https://www.svgrepo.com/show/373924/nginx.svg",
    #     },
    #     {
    #         "id": 3,
    #         "name": "GitHub",
    #         "img": "https://cdn-icons-png.flaticon.com/512/25/25231.png",
    #     },
    # ]
    # random.shuffle(items)

    db_path = Path(__file__).parent.parent / 'database'  / 'weights.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT device_id, weight, timestamp FROM weight_data ORDER BY timestamp DESC LIMIT 10")
    data = cursor.fetchall()
    conn.close()

    return [{"device_id": row[0], "weight": row[1], "timestamp": row[2]} for row in data]


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
