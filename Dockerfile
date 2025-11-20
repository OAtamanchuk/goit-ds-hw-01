# Базовий образ
FROM python:3.11

WORKDIR /app

COPY . /app

RUN pip install pipenv && pipenv install --system --deploy

CMD ["python", "main.py"]
