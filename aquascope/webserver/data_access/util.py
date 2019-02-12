import os

import dateutil
import pandas as pd
from PIL import Image

from aquascope.webserver.data_access.conversions import (item_to_blob_name,
                                                         group_id_to_container_name)
from aquascope.webserver.data_access.db import Item
from aquascope.webserver.data_access.db.items import TAXONOMY_FIELDS, ADDITIONAL_ATTRIBUTES_FIELDS
from aquascope.webserver.data_access.storage.blob import create_container, upload_blob, exists


def populate_db_with_items(items, db):
    items_dicts = [item.get_dict() for item in items]
    db.items.insert_many(items_dicts)


def populate_db_with_uploads(uploads, db):
    uploads_dicts = [upload.get_dict() for upload in uploads]
    db.uploads.insert_many(uploads_dicts)


def populate_system_with_items(data_dir, db, storage_client=None):
    features_path = os.path.join(data_dir, 'features.tsv')
    images = os.listdir(data_dir)
    images.remove('features.tsv')

    converters = {
        'timestamp': lambda x: dateutil.parser.parse(x),
        'url': lambda x: os.path.basename(x)
    }
    df = pd.read_csv(features_path, converters=converters, sep='\t')

    for field in TAXONOMY_FIELDS + ADDITIONAL_ATTRIBUTES_FIELDS:
        if field not in df.columns:
            df[field] = None

    items = []
    for item in list(df.to_dict('index').values()):
        image_path = os.path.join(data_dir, os.path.basename(item['url']))
        if not os.path.exists(image_path):
            continue

        image = Image.open(image_path)
        width, height = image.size
        items.append(Item.from_tsv_row(item, width, height))

    container_name = group_id_to_container_name(items[0].group_id)
    if storage_client and not exists(storage_client, container_name):
        create_container(storage_client, container_name)

    for item in items:
        result = db.items.insert_one(item.get_dict())
        item._id = result.inserted_id
        blob_name = item_to_blob_name(item)

        image_path = os.path.join(data_dir, item.filename)
        blob_meta = dict(filename=item.filename)
        if storage_client:
            upload_blob(storage_client, container_name, blob_name, image_path, blob_meta)
