from test_celery_task import add

res = add.delay(4, 6)

print(res.get(propagate=False))
