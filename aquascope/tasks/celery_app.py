import os

from aquascope.tasks.celery import make_celery_app

celery_user = os.environ['CELERY_USER']
celery_password = os.environ['CELERY_PASS']
celery_address = os.environ['CELERY_ADDRESS']
celery_app = make_celery_app(celery_user, celery_password, celery_address)
