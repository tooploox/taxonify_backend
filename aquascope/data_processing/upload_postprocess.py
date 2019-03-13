import os
import tarfile
import tempfile

from pandas.errors import EmptyDataError
from pymongo.errors import WriteError

from aquascope.webserver.data_access.db import upload
from aquascope.webserver.data_access.storage import blob
from aquascope.webserver.data_access.util import (populate_system_with_items, MissingTsvFileError,
                                                  upload_data_dir_to_items)


def download_and_extract_upload(upload_id, container_name, download_path, extraction_path, storage_client):
    blob.download_blob(storage_client, container_name, upload_id, download_path)

    with tarfile.open(download_path, "r:bz2") as tar:
        tar.extractall(extraction_path)


def extraction_path_to_data_path(extr_path):
    data_dir = os.listdir(extr_path)[0]
    data_dir = os.path.join(extr_path, data_dir)
    return data_dir


def parse_upload_package(upload_id, db, storage_client):
    upload.update_state(db, upload_id, 'processing')

    with tempfile.TemporaryDirectory() as tmpdirname:
        local_filepath = os.path.join(tmpdirname, 'localfile')
        extraction_path = os.path.join(tmpdirname, 'extracted')
        container_name = blob.group_id_to_container_name('upload')

        try:
            download_and_extract_upload(upload_id, container_name, local_filepath, extraction_path, storage_client)
            data_path = extraction_path_to_data_path(extraction_path)
            result = populate_system_with_items(upload_id, data_path, db, storage_client)
        except (tarfile.ReadError, WriteError, MissingTsvFileError,
                FileNotFoundError, OSError, IndexError, EmptyDataError):
            upload.update_state(db, upload_id, 'failed')
            return

    upload.update_state(db, upload_id, 'finished', **result)


def upload_id_to_item_filenames(storage_client, upload_id):
    with tempfile.TemporaryDirectory() as tmpdirname:
        local_filepath = os.path.join(tmpdirname, 'localfile')
        extraction_path = os.path.join(tmpdirname, 'extracted')
        container_name = blob.group_id_to_container_name('upload')

        try:
            download_and_extract_upload(upload_id, container_name, local_filepath, extraction_path,
                                        storage_client)
            data_path = extraction_path_to_data_path(extraction_path)
            items = upload_data_dir_to_items(data_path, upload_id)
            return [item.filename for item in items]
        except (tarfile.ReadError, MissingTsvFileError, FileNotFoundError, EmptyDataError):
            return []
