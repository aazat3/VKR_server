from flask import Flask, jsonify
import sqlite3
from pathlib import Path

app = Flask(__name__)

@app.route('/api/weights', methods=['GET'])
def get_weights():
    # db_path = Path(__file__).parent.parent / 'scale_server'  / 'weights.db'
    
    # conn = sqlite3.connect("db_path")
    # cursor = conn.cursor()
    # cursor.execute("SELECT device_id, weight, timestamp FROM weight_data ORDER BY timestamp DESC LIMIT 10")
    # data = cursor.fetchall()
    # conn.close()

    data = [
            {"device_id": 1, "weight": 70.5, "timestamp": "2025-02-15T12:00:00"},
            {"device_id": 2, "weight": 65.3, "timestamp": "2025-02-15T12:05:00"}
        ]
    return jsonify(data)
    # return jsonify([{"device_id": d[0], "weight": d[1], "timestamp": d[2]} for d in data])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
