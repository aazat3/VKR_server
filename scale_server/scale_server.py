import sqlite3
import paho.mqtt.client as mqtt
from pathlib import Path
import logging

# Callback при подключении к брокеру
def on_connect(client, userdata, flags, reason_code, properties):
    print("Connected with result code " + str(reason_code))
    client.subscribe("iot/+/weight")  # Подписка на все устройства


# Функция обработки сообщений
def on_message(client, userdata, msg):
    device_id = msg.topic.split("/")[1]
    weight = float(msg.payload.decode())

    cursor.execute("INSERT INTO weight_data (device_id, weight) VALUES (?, ?)", (device_id, weight))
    conn.commit()

    print(f"Stored: {device_id} - {weight}")


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Подключение к базе данных (или создание)
db_path = Path(__file__).parent.parent / 'database'  / 'weights.db'
logger.info(db_path)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS weight_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        device_id TEXT,
        weight FLOAT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
""")
conn.commit()

# Создание MQTT-клиента
client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
# client.on_connect = lambda c, u, f, rc: c.subscribe("iot/+/weight")
client.on_message = on_message

client.connect("localhost", 1883, 60)  # Подключение к брокеру Mosquitto
client.loop_forever()  # Запуск бесконечного цикла
