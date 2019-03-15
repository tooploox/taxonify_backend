import logging
import traceback

from aquascope.data_processing.upload_postprocess import parse_upload_package
from aquascope.tasks.celery_app import celery_app
from aquascope.webserver.data_access.db.util import get_db_from_env, get_storage_client_from_env

logging.getLogger("azure.storage").setLevel(logging.CRITICAL)

logger = logging.getLogger("celery.logger")
handler = logging.handlers.RotatingFileHandler('logs/celery.log', maxBytes=1000000, backupCount=1)
formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


@celery_app.task
def parse_upload(upload_id):
    db = get_db_from_env()
    storage_client = get_storage_client_from_env()
    try:
        parse_upload_package(upload_id, db, storage_client)
    except:
        logger.error(traceback.format_exc())

