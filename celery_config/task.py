import os
from celery import Celery
import config


app = Celery(
    "task",
    broker=os.getenv("CELERY_BROKER_URL"),
    backend="rpc://",
)

app.autodiscover_tasks(["home_task.tasks"])


def get_celery_app():
    return app


