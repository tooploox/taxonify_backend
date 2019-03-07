import os
from collections import OrderedDict

from pymongo import MongoClient, ASCENDING
from pymongo.errors import CollectionInvalid, OperationFailure

from aquascope.webserver.data_access.db.items import ITEMS_DB_SCHEMA
from aquascope.webserver.data_access.db.upload import UPLOAD_DB_SCHEMA
from aquascope.webserver.data_access.db.users import USERS_DB_SCHEMA


def override_collection_validator(db, collection_name, validator_json_schema):
    query = [('collMod', collection_name),
             ('validator', {'$jsonSchema': validator_json_schema}),
             ('validationLevel', 'strict')]
    query = OrderedDict(query)
    db.command(query)


def create_collections(db):
    collections_with_schemas = [
        ('items', ITEMS_DB_SCHEMA),
        ('uploads', UPLOAD_DB_SCHEMA),
        ('users', USERS_DB_SCHEMA)
    ]

    for (collection, schema) in collections_with_schemas:
        try:
            db.create_collection(collection)
            override_collection_validator(db, collection, schema)
        except (CollectionInvalid, OperationFailure):
            pass

    db.users.create_index([('username', ASCENDING)], unique=True)
    db.items.create_index([('filename', ASCENDING)], unique=True)


def get_db(connection_string, with_create_collections=True):
    mongo_client = MongoClient(connection_string)
    db = mongo_client.get_database()
    if with_create_collections:
        create_collections(db)
    return db


def get_db_from_env(with_create_collections=True):
    mongo_connection_string = os.environ['MONGO_CONNECTION_STRING']
    return get_db(mongo_connection_string, with_create_collections=with_create_collections)


def project_dict(item_dict, projection):
    for k, v in projection.items():
        if k in item_dict and v == 0:
            item_dict.pop(k, None)

    return item_dict
