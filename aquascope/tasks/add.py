import time

from aquascope.tasks.celery_app import celery_app


@celery_app.task
def task(x, y):
    time.sleep(2)
    print("it's my adding task")
    return x + y
