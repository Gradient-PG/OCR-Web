FROM python:3.10-alpine3.13
LABEL maintainer="chriskondracki"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app

RUN apk update && \
    apk add --no-cache openssl && \
    apk add --no-cache gcc musl-dev libffi-dev && \
    python -m venv /py && \
    pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    pip install -r /tmp/requirements.dev.txt && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        flaskuser



USER flaskuser

