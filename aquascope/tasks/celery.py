from celery import Celery


def make_celery_app(user, password, address):
    return Celery('aquascope',
                  backend='rpc://',
                  broker=f'pyamqp://{user}:{password}@{address}',
                  include=['aquascope.tasks.add',
                           'aquascope.tasks.upload_postprocess'])
