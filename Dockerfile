ARG PYTHON_VERSION=3.10.12
FROM python:${PYTHON_VERSION}-slim as base

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt update \
    && apt -y install build-essential

COPY requirements.txt /app/requirements.txt

RUN python -m pip install -r requirements.txt

COPY . .