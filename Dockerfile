ARG PYTHON_VERSION=3.10.12
FROM python:${PYTHON_VERSION}-slim as base

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# RUN mkdir -p public_html

RUN apt update \
    && apt -y install build-essential

COPY . .

RUN python -m pip install -r requirements.txt

EXPOSE 8000