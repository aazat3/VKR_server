FROM python:3.11.9-slim

# Устанавливаем зависимости
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код в контейнер
COPY . /app
WORKDIR /app

# Скрипт для скачивания модели при необходимости
RUN mkdir -p /opt/vosk-model-ru
RUN apt-get update && apt-get install -y wget unzip

COPY download_model.sh /opt/vosk-model-ru/download_model.sh
RUN chmod +x /opt/vosk-model-ru/download_model.sh

# Собираем команду для скачивания модели и старта сервера
CMD /opt/vosk-model-ru/download_model.sh && python scale_server.py /opt/vosk-model-ru/model
