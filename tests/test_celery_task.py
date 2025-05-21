from celery_config import Celery

app = Celery("test_celery_task", broker="pyamqp://guest@localhost//", backend="rpc://")


def get_celery_app():
    return app
