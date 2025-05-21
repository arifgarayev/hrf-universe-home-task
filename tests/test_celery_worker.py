from celery_config import Celery

app = Celery(
    "test_celery_task",
    broker="pyamqp://guest@localhost//",
    backend="rpc://"
)

# @app.test_celery
# def add(x, y):
#     return x + y

# def start_worker():

#     worker = app.Worker(
#         pool="solo",          
#         loglevel="INFO",
#         hostname="worker1@%h",
#     )
#     worker.start()            

# if __name__ == "__main__":
#     # print("Starting Celery worker…")
#     # start_worker()
#     res = add.apply_async((4, 6))  
#     res.get(timeout=10) 
