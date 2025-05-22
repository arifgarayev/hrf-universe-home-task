import json
from celery_config.task import get_celery_app
from celery import shared_task
from home_task.transactions.insert import HireStatisticsInsert
from home_task.db import get_session
from celery_config.task import app

# app = get_celery_app()
db_session = get_session()

@app.task(name="insert_hire_statistics", serializer="json")
def insert_hire_statistics(stats: list[dict]):
    stats = json.loads(stats)
    
    insert = HireStatisticsInsert(db_session)
    session = insert.insert(stats)

    

    session.commit()

    return {}

