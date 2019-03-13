import logging

from aquascope.data_processing.upload_postprocess import parse_upload_package
from aquascope.tasks.celery_app import celery_app
from aquascope.webserver.data_access.db.util import get_db_from_env, get_storage_client_from_env

logging.getLogger("azure.storage").setLevel(logging.CRITICAL)


@celery_app.task
def parse_upload(upload_id):
    db = get_db_from_env()
    storage_client = get_storage_client_from_env()
    parse_upload_package(upload_id, db, storage_client)
