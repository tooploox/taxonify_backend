from aquascope.tasks.celery_app import celery_app


@celery_app.task
def parse_upload(upload_id):
    pass
