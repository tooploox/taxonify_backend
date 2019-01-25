import os

import fire
from pymongo import MongoClient

from aquascope.webserver.data_access.storage.blob import blob_storage_client
from aquascope.webserver.data_access.util import populate_system


def run_populate_system(metadata_csv, images_directory):
    mongo_connection_string = os.environ['MONGO_CONNECTION_STRING']
    mongo_client = MongoClient(mongo_connection_string)
    db = mongo_client.get_database()

    storage_client = blob_storage_client(connection_string=os.environ['STORAGE_CONNECTION_STRING'])
    populate_system(metadata_csv, images_directory, db, storage_client)


if __name__ == '__main__':
    fire.Fire(run_populate_system)
