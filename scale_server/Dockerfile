FROM python:3.11.9-slim

# Устанавливаем зависимости
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Копируем код в контейнер
COPY . .

# Устанавливаем переменную окружения для отключения буферизации вывода
ENV PYTHONUNBUFFERED=1


CMD [ "python", "test_scale_server.py" ]