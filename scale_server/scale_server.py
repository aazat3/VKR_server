import asyncio
import websockets
from websockets.legacy.server import WebSocketServerProtocol
import logging
import json
from SQL.products.dao import *
from vosk import Model, SpkModel, KaldiRecognizer
import wave
import concurrent.futures
import os
import sys
from datetime import datetime, timezone


logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Таймауты и другие параметры
CONNECTION_TIMEOUT = 10  # Время ожидания активности от клиента в секундах
INACTIVITY_TIMEOUT = 10  # Время неактивности соединения до его закрытия

def process_chunk(rec, payload):    
    try:
        if payload == '{"eof" : 1}':
            logging.info('{"eof" : 1}')
            finalRecResult = rec.FinalResult()
            logging.info(finalRecResult)
            return finalRecResult, True
        if payload == '{"reset" : 1}':
            return rec.FinalResult(), False
        if rec.AcceptWaveform(payload):
            recResult = rec.Result()
            logging.info(recResult)
            return recResult, False
        else:
            return rec.PartialResult(), False
    except Exception as e:
        logging.error(f"❌ Ошибка обработки аудио: {e}")
        return '{"error": "processing error"}', False
    

async def recognize(websocket: WebSocketServerProtocol, path=None):
    """Обрабатывает сообщения от конкретного IoT-устройства"""
    logging.info(f"✅ Начало обработки устройства {websocket.remote_address}")
    
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
    mainResponse = ""
    try:
        while True:
            try:
                # Ждем сообщение, но не дольше 7 секунд
                message = await asyncio.wait_for(websocket.recv(), timeout=INACTIVITY_TIMEOUT)
            except asyncio.TimeoutError:
                logging.info(f"⚠ Тайм-аут {INACTIVITY_TIMEOUT} сек. Закрываем соединение: {websocket.remote_address}")
                break  # Выходим из цикла
            # Load configuration if provided
            if isinstance(message, str):
                if 'config' in message:
                    jobj = json.loads(message)['config']
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
                if 'id' in message:
                    json.loads(message)
                    logging.info(message)
                    continue

            # Create the recognizer, word list is temporary disabled since not every model supports it
            if not rec or model_changed:
                model_changed = False
                if phrase_list:
                    rec = KaldiRecognizer(model, sample_rate, json.dumps(phrase_list, ensure_ascii=False))
                else:
                    rec = KaldiRecognizer(model, sample_rate)
                rec.SetWords(show_words)
                rec.SetMaxAlternatives(max_alternatives)
                if spk_model:
                    rec.SetSpkModel(spk_model)

            response = await loop.run_in_executor(pool, process_chunk, rec, message)
            if ("result" in json.loads(response[0])):
                mainResponse = response[0]

            if response[1]: 
                textResponse = str(json.loads(mainResponse)["text"])
                logging.info(f"Response: {textResponse}")
                await websocket.send(textResponse)
                await search(textResponse)
                break
    except websockets.exceptions.ConnectionClosedError:
        logging.info(f"Соединение закрыто: {websocket.remote_address}")
    except Exception as e:
        logging.error(f"Ошибка: {e}")
    finally:
        await websocket.close()  # Явно закрыть соединение
        logging.info(f"⚠ Завершаем {websocket.remote_address}")

async def search(q: str):
    sc_result = await ProductsDAO.search_products_by_name(q)
    logging.info(sc_result)

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

    args.interface = os.environ.get('VOSK_SERVER_INTERFACE', '0.0.0.0')
    args.port = int(os.environ.get('VOSK_SERVER_PORT', 5000))
    args.model_path = os.environ.get('VOSK_MODEL_PATH', 'model')
    args.spk_model_path = os.environ.get('VOSK_SPK_MODEL_PATH')
    args.sample_rate = float(os.environ.get('VOSK_SAMPLE_RATE', 16000))
    args.max_alternatives = int(os.environ.get('VOSK_ALTERNATIVES', 0))
    args.show_words = bool(os.environ.get('VOSK_SHOW_WORDS', True))

    # if len(sys.argv) > 1:
    #    args.model_path = sys.argv[1]

    try:
        model = Model(args.model_path)
        logging.info(f"Модель загружена успешно с пути: {args.model_path}")
    except Exception as e:
        logging.error(f"❌ Ошибка загрузки модели: {e}")
        
    spk_model = SpkModel(args.spk_model_path) if args.spk_model_path else None
    pool = concurrent.futures.ThreadPoolExecutor((os.cpu_count() or 1))

    try:
        async with websockets.serve(recognize, args.interface, args.port):
            await asyncio.Future()
    finally:
        pool.shutdown(wait=True)  # Корректное завершение ThreadPool
        if 'model' in globals():
            del model  # Освобождение памяти модели

   
asyncio.run(main())
