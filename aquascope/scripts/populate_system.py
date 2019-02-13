import os

import fire

from aquascope.webserver.data_access.db.util import get_db_from_env
from aquascope.webserver.data_access.storage.blob import blob_storage_client
from aquascope.webserver.data_access.util import populate_system_with_items


def run_populate_system(data_directory):
    db = get_db_from_env()

    storage_client = blob_storage_client(connection_string=os.environ['STORAGE_CONNECTION_STRING'])
    populate_system_with_items(data_directory, db, storage_client)


if __name__ == '__main__':
    fire.Fire(run_populate_system)
