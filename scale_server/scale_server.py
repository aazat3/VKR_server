import sqlite3
import asyncio
import aiomqtt
# from pathlib import Path
import logging
from sqlalchemy.orm import Session
import json
from SQL import database, models, schemas, crud

# .\mosquitto_pub -h aazatserver.ru -t "iot/device1/weight" -m '{"name": "orange", "calories": 56}' -u "admin" -P "admin"
# .\mosquitto_pub -h aazatserver.ru -t "iot/device1/weight" -m '{\"name\": \"orange\", \"calories\": 56}' -u "admin" -P "admin"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def save_to_db(payload):
    with database.SessionLocal() as db:
        try:
            product = models.Product(
                name = payload["name"],
                calories = payload["calories"]
            )
            db.add(product)
            db.commit()
            db.refresh(product)
        except:
            db.rollback()
            logger.info("Ошибка сохранения: {e}")
        finally:
            db.close()
        # crud.create_product(db, product)


async def main():
    async with aiomqtt.Client(
        hostname="aazatserver.ru",
        port=1883,
        username="admin",
        password="admin"
    ) as client:
        await client.subscribe("iot/+/weight")
        logger.info("subscribe")
        async for message in client.messages:
            payload = json.loads(message.payload.decode())
            # save_to_db(payload)
            logger.info("get message")




asyncio.run(main())

# Callback при подключении к брокеру
# def on_connect(client, userdata, flags, reason_code, properties):
#     logger.info("Connected with result code " + str(reason_code))
#     client.subscribe("iot/+/weight")  # Подписка на все устройства


# # Функция обработки сообщений
# def on_message(client, userdata, msg):
#     logger.info("get message")
#     logger.info(msg.payload.decode())

#     # device_id = msg.topic.split("/")[1]
#     # weight = float(msg.payload.decode())
#     payload = json.loads(msg.payload.decode())
#     save_to_db(payload)


# # Создание MQTT-клиента
# client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
# client.on_connect = on_connect
# # client.on_connect = lambda c, u, f, rc: c.subscribe("iot/+/weight")
# client.on_message = on_message
# client.username_pw_set("admin", "admin")
# client.connect("aazatserver.ru", 1883, 60)  # Подключение к брокеру Mosquitto
# client.loop_forever()  # Запуск бесконечного цикла