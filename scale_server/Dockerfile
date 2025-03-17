FROM python:3.11.9-slim

# Устанавливаем зависимости
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Копируем код в контейнер
COPY . /app
WORKDIR /app


# Устанавливаем переменную окружения для отключения буферизации вывода
ENV PYTHONUNBUFFERED=1


CMD [ "python", "api_server.py" ]