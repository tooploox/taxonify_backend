import logging
import os
import tarfile
import tempfile

from pymongo.errors import WriteError

from aquascope.tasks.celery_app import celery_app
from aquascope.webserver.data_access.db.util import get_db_from_env
from aquascope.webserver.data_access.db import upload
from aquascope.webserver.data_access.storage import blob
from aquascope.webserver.data_access.storage.blob import blob_storage_client
from aquascope.webserver.data_access.util import populate_system_with_items

logging.getLogger("azure.storage").setLevel(logging.CRITICAL)


def get_storage_client():
    storage_connection_string = os.environ['STORAGE_CONNECTION_STRING']
    return blob_storage_client(connection_string=storage_connection_string)


def extraction_path_to_data_path(extraction_path):
    data_dir = os.listdir(extraction_path)[0]
    data_dir = os.path.join(extraction_path, data_dir)
    return data_dir


@celery_app.task
def parse_upload(upload_id):
    db = get_db_from_env()
    upload.update_state(db, upload_id, 'processing')
    storage_client = get_storage_client()

    with tempfile.TemporaryDirectory() as tmpdirname:
        local_filepath = os.path.join(tmpdirname, 'localfile')
        extraction_path = os.path.join(tmpdirname, 'extracted')
        container_name = blob.group_id_to_container_name('upload')
        blob.download_blob(storage_client, container_name, upload_id, local_filepath)

        try:
            with tarfile.open(local_filepath, "r:bz2") as tar:
                tar.extractall(extraction_path)
            data_path = extraction_path_to_data_path(extraction_path)
            populate_system_with_items(data_path, db, storage_client)
        except (tarfile.ReadError, WriteError) as e:
            upload.update_state(db, upload_id, 'failed')
            return

    upload.update_state(db, upload_id, 'finished')
