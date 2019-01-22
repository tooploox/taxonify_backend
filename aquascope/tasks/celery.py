import os

from celery import Celery

celery_app = Celery('aquascope',
                    backend='rpc://',
                    broker='pyamqp://{}:{}@{}'.format(
                        os.environ['CELERY_USER'],
                        os.environ['CELERY_PASS'],
                        os.environ['CELERY_ADDRESS']),
                    include=['aquascope.tasks.add'])
