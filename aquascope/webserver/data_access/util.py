import copy
import math
import os

import dateutil
import pandas as pd
from PIL import Image
from bson import ObjectId
from pymongo.errors import DuplicateKeyError

from aquascope.webserver.data_access.conversions import (item_id_and_extension_to_blob_name,
                                                         group_id_to_container_name)
from aquascope.webserver.data_access.db import Item, upload
from aquascope.webserver.data_access.db.items import ANNOTABLE_FIELDS, MORPHOMETRIC_FIELDS
from aquascope.webserver.data_access.storage import blob
from aquascope.webserver.data_access.storage.blob import create_container, upload_blob, exists


class MissingTsvFileError(ValueError):
    pass


def populate_db_with_items(items, db):
    items_dicts = [copy.deepcopy(item.get_dict()) for item in items]
    db.items.insert_many(items_dicts)


def populate_db_with_uploads(uploads, db):
    uploads_dicts = [copy.deepcopy(upload.get_dict()) for upload in uploads]
    db.uploads.insert_many(uploads_dicts)


def populate_db_with_users(users, db):
    users_dicts = [copy.deepcopy(user) for user in users]
    db.users.insert_many(users_dicts)


def upload_package_from_stream(filename, stream, db, storage_client):
    container_name = blob.group_id_to_container_name('upload')
    if not blob.exists(storage_client, container_name):
        blob.create_container(storage_client, container_name)

    upload_doc = upload.create(db, filename)
    blob_filename = str(upload_doc.inserted_id)
    blob_meta = dict(filename=filename)
    blob.create_blob_from_stream(storage_client, container_name, blob_filename, stream,
                                 blob_meta)
    upload.update_state(db, blob_filename, 'uploaded')
    return blob_filename


def upload_data_dir_to_dataframe(data_dir):
    features_path = os.path.join(data_dir, 'features.tsv')
    images = os.listdir(data_dir)

    try:
        images.remove('features.tsv')
    except ValueError:
        raise MissingTsvFileError

    converters = {
        'timestamp': lambda x: dateutil.parser.parse(x),
        **{k: lambda x: float(x) if x else float('nan') for k in MORPHOMETRIC_FIELDS}
    }
    df = pd.read_csv(features_path, converters=converters, sep='\t')

    for field in ANNOTABLE_FIELDS:
        if field not in df.columns:
            df[field] = None
            df[f'{field}_modified_by'] = None
            df[f'{field}_modification_time'] = None

    return df


def split_items_to_valids_and_brokens(items):
    valids = []
    brokens = []
    for item in items:
        valid_fields = [math.isfinite(item[field]) for field in MORPHOMETRIC_FIELDS]
        valid = all(valid_fields)
        filename = item.filename
        valids.append(filename) if valid else brokens.append(filename)

    return valids, brokens


def upload_data_to_items_and_filepaths(data_dir, df, upload_id, upload_tags):
    items = []
    filepaths = []
    for item in list(df.to_dict('index').values()):

        image_path = os.path.join(data_dir, item['url'])
        if not os.path.exists(image_path):
            image_path = os.path.join(data_dir, os.path.basename(item['url']))

        image = Image.open(image_path)
        width, height = image.size
        items.append(Item.from_tsv_row(item, width, height, upload_id, upload_tags))
        filepaths.append(image_path)
    return items, filepaths


def populate_system_with_items(upload_id, data_dir, db, storage_client=None):
    upload_tags = upload.get_tags(db, ObjectId(upload_id))

    df = upload_data_dir_to_dataframe(data_dir)
    items, filepaths = upload_data_to_items_and_filepaths(data_dir, df, upload_id, upload_tags)

    container_name = group_id_to_container_name(items[0].group_id)
    if storage_client and not exists(storage_client, container_name):
        create_container(storage_client, container_name)

    duplicates = []
    valids, brokens = split_items_to_valids_and_brokens(items)
    for item, filepath in zip(items, filepaths):
        if item.filename in brokens:
            continue

        try:
            result = db.items.insert_one(item.get_dict())
        except DuplicateKeyError:
            duplicates.append(item.filename)
            continue

        item._id = result.inserted_id
        blob_name = item_id_and_extension_to_blob_name(item._id, item.extension)

        blob_meta = dict(filename=item.filename)
        if storage_client:
            upload_blob(storage_client, container_name, blob_name, filepath, blob_meta)

    return dict(image_count=len(items), duplicate_image_count=len(duplicates),
                duplicate_filenames=duplicates, broken_record_count=len(brokens),
                broken_records=brokens)
