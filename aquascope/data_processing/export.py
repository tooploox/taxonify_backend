import os
import tempfile

from aquascope.webserver.data_access.conversions import list_of_item_dicts_to_tsv
from aquascope.webserver.data_access.storage.export import upload_export_file


def export_items(items, storage_client):
    with tempfile.TemporaryDirectory() as tmpdirname:
        local_filepath = os.path.join(tmpdirname, 'features.tsv')
        list_of_item_dicts_to_tsv(items, local_filepath)
        return upload_export_file(storage_client, local_filepath)
