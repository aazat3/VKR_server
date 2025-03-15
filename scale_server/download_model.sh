#!/bin/bash

# Проверяем, существует ли модель
if [ ! -d "/opt/vosk-model-ru/model" ]; then
    echo "Скачиваем модель Vosk..."
    wget -q https://alphacephei.com/vosk/models/vosk-model-small-ru-0.22.zip -O /opt/vosk-model-ru/vosk-model.zip
    unzip /opt/vosk-model-ru/vosk-model.zip -d /opt/vosk-model-ru
    mv /opt/vosk-model-ru/vosk-model-small-ru-0.22 /opt/vosk-model-ru/model
    rm -rf /opt/vosk-model-ru/vosk-model.zip
fi
