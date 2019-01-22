from datetime import datetime, timedelta

from azure.storage.blob import BlobPermissions


def create_container(client, container_name):
    return client.create_container(container_name)


def generate_download_sas(client, container_name, blob_name, expiry_minutes=60):
    return client.generate_blob_shared_access_signature(container_name, blob_name,
                                                        permission=BlobPermissions.READ,
                                                        expiry=datetime.utcnow() + timedelta(minutes=expiry_minutes))


def generate_download_url(client, container_name, blob_name, sas_token):
    return client.make_blob_url(container_name, blob_name, sas_token=sas_token)
