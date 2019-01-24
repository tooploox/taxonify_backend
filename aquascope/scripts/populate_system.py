from datetime import datetime
import os

import fire
import numpy as np
import pandas as pd
from pymongo import MongoClient

from aquascope.webserver.data_access.conversions import (group_id_to_container_name,
                                                         item_to_blob_name)
from aquascope.webserver.data_access.db import Item
from aquascope.webserver.data_access.storage.blob import (blob_storage_client,
                                                          create_container, upload_blob)


def populate_system(metadata_csv, images_directory):
    mongo_connection_string = os.environ['MONGO_CONNECTION_STRING']
    mongo_client = MongoClient(mongo_connection_string)
    db = mongo_client.get_database()

    storage_client = blob_storage_client(connection_string=os.environ['STORAGE_CONNECTION_STRING'])

    converter = {'image_width': pd.to_numeric,
                 'image_height': pd.to_numeric}
    df = pd.read_csv(metadata_csv, converters=converter)
    df['acquisition_time'] = df['acquisition_time'].apply(lambda x: datetime.fromtimestamp(float(x)))
    df = df.replace({'TRUE': True, 'FALSE': False, 'null': None, np.nan: None})
    items = df.to_dict('records')
    items = [Item(item) for item in items]

    for item in items:
        image_path = os.path.join(images_directory, item.filename)
        if not os.path.exists(image_path):
            continue

        result = db.items.insert_one(item.get_dict())
        item._id = result.inserted_id
        blob_name = item_to_blob_name(item)

        container_name = group_id_to_container_name(item.group_id)
        create_container(storage_client, container_name)

        blob_meta = dict(filename=item.filename)
        upload_blob(storage_client, container_name, blob_name, image_path, blob_meta)


if __name__ == '__main__':
    fire.Fire(populate_system)
