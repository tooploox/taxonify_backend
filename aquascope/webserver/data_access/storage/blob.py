from datetime import datetime, timedelta

from azure.storage.blob import BlobPermissions
from azure.storage.blob.blockblobservice import BlockBlobService
from flask import current_app as app

from aquascope.webserver.data_access.conversions import item_to_blob_name, group_id_to_container_name


def blob_storage_client(connection_string):
    return BlockBlobService(connection_string=connection_string)


def create_container(client, container_name):
    return client.create_container(container_name)


def exists(client, container_name, blob_name=None):
    return client.exists(container_name, blob_name)


def generate_download_sas(client, container_name, blob_name, expiry_minutes=60):
    return client.generate_blob_shared_access_signature(container_name, blob_name,
                                                        permission=BlobPermissions.READ,
                                                        expiry=datetime.utcnow() + timedelta(minutes=expiry_minutes))


def generate_container_download_sas(client, container_name, expiry_minutes=60):
    return client.generate_container_shared_access_signature(container_name,
                                                             permission=BlobPermissions.READ,
                                                             expiry=datetime.utcnow() + timedelta(
                                                                 minutes=expiry_minutes))


def upload_blob(client, container_name, blob_name, filepath, metadata):
    return client.create_blob_from_path(container_name, blob_name, filepath,
                                        metadata=metadata)


def make_blob_url(client, container_name, blob_name, sas_token=None):
    return client.make_blob_url(container_name, blob_name, sas_token=sas_token)


def get_url_for_item(client, item):
    blob_name = item_to_blob_name(item)
    container_name = group_id_to_container_name(item.group_id)
    return make_blob_url(client, container_name, blob_name)


def get_urls_for_items(items):
    client = app.config['storage_client']
    return {str(item._id): get_url_for_item(client, item) for item in items}
