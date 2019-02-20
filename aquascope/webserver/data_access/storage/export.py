import uuid

from aquascope.webserver.data_access.conversions import group_id_to_container_name
from aquascope.webserver.data_access.storage.blob import exists, create_container, upload_blob, generate_download_sas, \
    make_blob_url

EXPORT_SAS_EXPIRY_MINUTES = 1440


def upload_export_file(client, local_filepath):
    container_name = group_id_to_container_name('download')
    if not exists(client, container_name):
        create_container(client, container_name)

    blob_name = str(uuid.uuid1()) + '.tsv'
    upload_blob(client, container_name, blob_name, local_filepath, None)

    sas = generate_download_sas(client, container_name, blob_name,
                                EXPORT_SAS_EXPIRY_MINUTES)

    return make_blob_url(client, container_name, blob_name, sas)
