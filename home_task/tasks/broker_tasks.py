from celery_config.task import get_celery_app
from home_task.transactions.insert import HireStatisticsInsert
from home_task.db import get_session

app = get_celery_app()
db_session = get_session()

@app.task
def insert_hire_statistics(stats: list[dict]):
    
    insert = HireStatisticsInsert(db_session)
    insert.insert(stats)

