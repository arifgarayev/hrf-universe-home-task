import os

from celery import Celery

import config  # to execute the config.py file

app = Celery(
    "task",
    broker=f'{os.getenv("MQ_DRIVER")}://{os.getenv("MQ_USER")}@{os.getenv("MQ_HOST") if not os.getenv("IS_LOCAL") else "localhost"}//',
    backend="rpc://",
)


def get_celery_app():
    return app
