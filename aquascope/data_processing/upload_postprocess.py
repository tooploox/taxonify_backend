import os
import tarfile
import tempfile

from pymongo.errors import WriteError

from aquascope.webserver.data_access.db import upload
from aquascope.webserver.data_access.storage import blob
from aquascope.webserver.data_access.util import populate_system_with_items, MissingTsvFileError


def extraction_path_to_data_path(extraction_path):
    data_dir = os.listdir(extraction_path)[0]
    data_dir = os.path.join(extraction_path, data_dir)
    return data_dir


def parse_upload_package(upload_id, db, storage_client):
    upload.update_state(db, upload_id, 'processing')

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
        except (tarfile.ReadError, WriteError, MissingTsvFileError,
                FileNotFoundError, OSError):
            upload.update_state(db, upload_id, 'failed')
            return

    upload.update_state(db, upload_id, 'finished')
