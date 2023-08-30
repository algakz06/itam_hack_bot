# Separate "build" image
FROM python:3.11-slim-bullseye


COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

WORKDIR /app

COPY . .

