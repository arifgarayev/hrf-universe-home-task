import json

from celery import shared_task

from celery_config.task import app, get_celery_app
from home_task.db import get_session
from home_task.transactions.insert import HireStatisticsInsert

# app = get_celery_app()
db_session = get_session()


@app.task(name="insert_hire_statistics", serializer="json")
def insert_hire_statistics(stats: list[dict]):
    stats = json.loads(stats)

    insert = HireStatisticsInsert(db_session)
    session = insert.insert(stats)

    session.commit()

    return {}
