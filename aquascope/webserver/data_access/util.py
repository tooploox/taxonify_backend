from datetime import datetime
import os

import numpy as np
import pandas as pd

from aquascope.webserver.data_access.conversions import (item_to_blob_name,
                                                         group_id_to_container_name)
from aquascope.webserver.data_access.db import Item
from aquascope.webserver.data_access.storage.blob import create_container, upload_blob


def populate_db_with_items(items, db):
    items_dicts = [item.get_dict() for item in items]
    db.items.insert_many(items_dicts)


def populate_system(metadata_csv, images_directory, db, storage_client=None):
    converter = {'image_width': pd.to_numeric,
                 'image_height': pd.to_numeric,
                 'acquisition_time': lambda x: datetime.fromtimestamp(float(x))
                 }
    df = pd.read_csv(metadata_csv, converters=converter)
    df = df.replace({'TRUE': True, 'FALSE': False, 'null': None, np.nan: None})
    items = df.to_dict('index').values()
    items = [Item(item) for item in items]

    for item in items:
        image_path = os.path.join(images_directory, item.filename)
        if not os.path.exists(image_path):
            continue

        result = db.items.insert_one(item.get_dict())
        item._id = result.inserted_id
        blob_name = item_to_blob_name(item)

        container_name = group_id_to_container_name(item.group_id)

        if storage_client:
            create_container(storage_client, container_name)

        blob_meta = dict(filename=item.filename)
        if storage_client:
            upload_blob(storage_client, container_name, blob_name, image_path, blob_meta)
