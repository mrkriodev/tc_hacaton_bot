FROM python:3.10-slim
LABEL authors="ghMixs"

RUN apt-get update && \
    apt-get install -y libpq-dev gcc curl

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

ENTRYPOIN python main.py