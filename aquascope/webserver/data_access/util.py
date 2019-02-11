from datetime import datetime
import os

import numpy as np
import pandas as pd

from aquascope.webserver.data_access.conversions import (item_to_blob_name,
                                                         group_id_to_container_name)
from aquascope.webserver.data_access.db import Item
from aquascope.webserver.data_access.storage.blob import create_container, upload_blob, exists


def populate_db_with_items(items, db):
    items_dicts = [item.get_dict() for item in items]
    db.items.insert_many(items_dicts)


def populate_db_with_uploads(uploads, db):
    uploads_dicts = [upload.get_dict() for upload in uploads]
    db.uploads.insert_many(uploads_dicts)


def populate_system(metadata_csv, images_directory, db, storage_client=None):
    converter = {'image_width': pd.to_numeric,
                 'image_height': pd.to_numeric,
                 'acquisition_time': lambda x: datetime.fromtimestamp(float(x))
                 }
    taxonomy = ['empire', 'kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species']
    taxonomy_converter = {x: lambda x: str(x).lower() for x in taxonomy}
    converter = {**converter, **taxonomy_converter}
    df = pd.read_csv(metadata_csv, converters=converter)
    df = df.replace({'TRUE': True, 'FALSE': False, 'null': None, np.nan: None})

    items = df.to_dict('index').values()
    items = [Item(item) for item in items]

    container_name = group_id_to_container_name(items[0].group_id)

    if storage_client and not exists(storage_client, container_name):
        create_container(storage_client, container_name)

    db.items.drop()
    for item in items:
        image_path = os.path.join(images_directory, item.filename)
        if not os.path.exists(image_path):
            continue

        result = db.items.insert_one(item.get_dict())
        item._id = result.inserted_id
        blob_name = item_to_blob_name(item)

        blob_meta = dict(filename=item.filename)
        if storage_client:
            upload_blob(storage_client, container_name, blob_name, image_path, blob_meta)
