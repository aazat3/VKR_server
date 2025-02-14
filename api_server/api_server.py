import random
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


app = FastAPI()


@app.get("/items")
def get_items():
    items = [
        {
            "id": 1,
            "name": "Docker",
            "img": "https://static-00.iconduck.com/assets.00/docker-icon-2048x2048-5mc7mvtn.png",
        },
        {
            "id": 2,
            "name": "Nginx",
            "img": "https://www.svgrepo.com/show/373924/nginx.svg",
        },
        {
            "id": 3,
            "name": "GitHub",
            "img": "https://cdn-icons-png.flaticon.com/512/25/25231.png",
        },
    ]
    random.shuffle(items)
    return items


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


# from flask import Flask, jsonify
# import sqlite3
# from pathlib import Path

# app = Flask(__name__)

# @app.route('/api/weights', methods=['GET'])
# def get_weights():
#     # db_path = Path(__file__).parent.parent / 'scale_server'  / 'weights.db'
    
#     # conn = sqlite3.connect("db_path")
#     # cursor = conn.cursor()
#     # cursor.execute("SELECT device_id, weight, timestamp FROM weight_data ORDER BY timestamp DESC LIMIT 10")
#     # data = cursor.fetchall()
#     # conn.close()

#     data = [
#             {"device_id": 1, "weight": 70.5, "timestamp": "2025-02-15T12:00:00"},
#             {"device_id": 2, "weight": 65.3, "timestamp": "2025-02-15T12:05:00"}
#         ]
#     return jsonify(data)
#     # return jsonify([{"device_id": d[0], "weight": d[1], "timestamp": d[2]} for d in data])
#     return 'Hello, World!'

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)
