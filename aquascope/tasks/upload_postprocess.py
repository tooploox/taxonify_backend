import logging
import os

from aquascope.data_processing.upload_postprocess import parse_upload_package
from aquascope.tasks.celery_app import celery_app
from aquascope.webserver.data_access.db.util import get_db_from_env
from aquascope.webserver.data_access.storage.blob import blob_storage_client

logging.getLogger("azure.storage").setLevel(logging.CRITICAL)


def get_storage_client():
    storage_connection_string = os.environ['STORAGE_CONNECTION_STRING']
    return blob_storage_client(connection_string=storage_connection_string)


@celery_app.task
def parse_upload(upload_id):
    db = get_db_from_env()
    storage_client = get_storage_client()
    parse_upload_package(upload_id, db, storage_client)
