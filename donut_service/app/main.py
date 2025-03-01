import logging
import os

from fastapi import FastAPI
from fastapi.logger import logger

from .routers import (
    dataset,
)

# TODO: set LOG_LEVEL in Dockerfile/docker-compose
# TODO: make it work: https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker/issues/19#issuecomment-606672830
os.environ['LOG_LEVEL'] = 'DEBUG'
gunicorn_logger = logging.getLogger('gunicorn.error')
logger.handlers = gunicorn_logger.handlers
if __name__ != 'main':
    logger.setLevel(gunicorn_logger.level)
else:
    logger.setLevel(logging.DEBUG)

app = FastAPI(
    title='renameme',
    description='Fill the description',
    version='0.1',
)

app.include_router(dataset.router)