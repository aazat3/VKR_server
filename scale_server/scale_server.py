import asyncio
import aiomqtt
import logging
from sqlalchemy.orm import Session
import json
from SQL import database, models, schemas, crud
from vosk import Model, SpkModel, KaldiRecognizer
import concurrent.futures
import os
import sys
from datetime import datetime, timezone



# .\mosquitto_pub -h aazatserver.ru -t "iot/device1/weight" -m '{"name": "orange", "calories": 56}' -u "admin" -P "admin"
# .\mosquitto_pub -h aazatserver.ru -t "iot/device1/weight" -m '{\"name\": \"orange\", \"calories\": 56}' -u "admin" -P "admin"

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

device_tasks = {}  # Словарь для хранения задач устройств
INACTIVITY_TIMEOUT = 30

def process_chunk(rec, message):
    logging.info(f"✅ обработка аудио")
    if message == '{"eof" : 1}':
        logging.info(f"вариант 1")
        return rec.FinalResult(), True
    if message == '{"reset" : 1}':
        logging.info(f"вариант 2")
        return rec.FinalResult(), False
    elif rec.AcceptWaveform(message):
        logging.info(f"вариант 3")
        return rec.Result(), False
    else:
        logging.info(f"вариант 4")
        return rec.PartialResult(), False
    

async def handle_device(client_id, message_queue):
    """Обрабатывает сообщения от конкретного IoT-устройства"""
    logging.info(f"✅ Начало обработки устройства {client_id}")
    
    global model
    global spk_model
    global args
    global pool

    loop = asyncio.get_running_loop()
    rec = None
    phrase_list = None
    sample_rate = args.sample_rate
    show_words = args.show_words
    max_alternatives = args.max_alternatives

    while True:
        try:
            # Ждём новое сообщение с тайм-аутом
            message = await asyncio.wait_for(message_queue.get(), timeout=INACTIVITY_TIMEOUT)
            payload = message.payload.decode()
            last_message_time = datetime.now(timezone.utc)  # Текущее время в UTC
            
            # Load configuration if provided
            if isinstance(payload, str) and 'config' in payload:
                jobj = json.loads(payload)['config']
                logging.info("Config %s", jobj)
                if 'phrase_list' in jobj:
                    phrase_list = jobj['phrase_list']
                if 'sample_rate' in jobj:
                    sample_rate = float(jobj['sample_rate'])
                if 'model' in jobj:
                    model = Model(jobj['model'])
                    model_changed = True
                if 'words' in jobj:
                    show_words = bool(jobj['words'])
                if 'max_alternatives' in jobj:
                    max_alternatives = int(jobj['max_alternatives'])
                continue

            # Create the recognizer, word list is temporary disabled since not every model supports it
            if not rec or model_changed:
                logging.info("Create rec_model")
                model_changed = False
                if phrase_list:
                    rec = KaldiRecognizer(model, sample_rate, json.dumps(phrase_list, ensure_ascii=False))
                    logging.info("Created rec_model")
                else:
                    rec = KaldiRecognizer(model, sample_rate)
                    logging.info("Created rec_model")
                rec.SetWords(show_words)
                rec.SetMaxAlternatives(max_alternatives)
                if spk_model:
                    rec.SetSpkModel(spk_model)

            response, stop = await loop.run_in_executor(pool, process_chunk, rec, payload)
            logging.info(response)
            if stop: break

        except asyncio.TimeoutError:
            # Если прошло слишком много времени без сообщений — завершаем задачу
            logging.info(f"⚠ Завершаем {client_id} (неактивен {INACTIVITY_TIMEOUT} сек.)")
            break

    # Очистка после завершения
    del device_tasks[client_id]
    del message_queue  # Явно удаляем очередь (необязательно, но можно)
    logging.info(f"🛑 Задача {client_id} завершена")


# def save_to_db(payload):
#     with database.SessionLocal() as db:
#         try:
#             product = models.Product(
#                 name = payload["name"],
#                 calories = payload["calories"]
#             )
#             db.add(product)
#             db.commit()
#             db.refresh(product)
#         except:
#             db.rollback()
#             logging.info("Ошибка сохранения: {e}")
#         finally:
#             db.close()
#         # crud.create_product(db, product)


async def main():
    global model
    global spk_model
    global args
    global pool
    
    args = type('', (), {})()

    args.model_path = os.environ.get('VOSK_MODEL_PATH', 'model')
    args.spk_model_path = os.environ.get('VOSK_SPK_MODEL_PATH')
    args.sample_rate = float(os.environ.get('VOSK_SAMPLE_RATE', 8000))
    args.max_alternatives = int(os.environ.get('VOSK_ALTERNATIVES', 0))
    args.show_words = bool(os.environ.get('VOSK_SHOW_WORDS', True))

    if len(sys.argv) > 1:
       args.model_path = sys.argv[1]

       
    model = Model(args.model_path)
    spk_model = SpkModel(args.spk_model_path) if args.spk_model_path else None
    pool = concurrent.futures.ThreadPoolExecutor((os.cpu_count() or 1))

    while True:
        try:
            async with aiomqtt.Client(
                hostname="aazatserver.ru",
                port=1883,
                username="admin",
                password="admin"
            ) as client:
                await client.subscribe("iot/+/audio")
                logging.info("susubscribe to iot/+/audio")
                async for message in client.messages:
                    logging.info(message.payload.decode())
                    # payload = json.loads(message.payload.decode())
                    # save_to_db(payload)
                    # logger.info(message.payload)
                    # client_id = message.topic.split("/")[-2]
                    client_id = str(message.topic).split("/")[-2]
                    if client_id not in device_tasks:
                        logging.info("New device")
                        message_queue = asyncio.Queue()
                        device_tasks[client_id] = asyncio.create_task(handle_device(client_id, message_queue))
                    await message_queue.put(message)
                    # asyncio.create_task(recognize(message))
        except Exception as e:
            logging.exception(f"Ошибка MQTT-соединения: {e}")
            await asyncio.sleep(5)  # Ждём перед повторным подключением


asyncio.run(main())
