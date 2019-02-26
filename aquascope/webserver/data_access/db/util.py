import os

import pymongo
from pymongo import MongoClient, ASCENDING
from pymongo.errors import CollectionInvalid

from aquascope.webserver.data_access.db.items import ITEMS_DB_SCHEMA
from aquascope.webserver.data_access.db.upload import UPLOAD_DB_SCHEMA
from aquascope.webserver.data_access.db.users import USERS_DB_SCHEMA


def create_collections(db):
    collections_with_schemas = [
        ('items', ITEMS_DB_SCHEMA),
        ('uploads', UPLOAD_DB_SCHEMA),
        ('users', USERS_DB_SCHEMA)
    ]

    for (collection, schema) in collections_with_schemas:
        try:
            db.create_collection(collection, validator={'$jsonSchema': schema})
        except CollectionInvalid:
            pass

    db.users.create_index([('username', ASCENDING)], unique=True)


def get_db(connection_string):
    mongo_client = MongoClient(connection_string)
    db = mongo_client.get_database()
    create_collections(db)
    return db


def get_db_from_env():
    mongo_connection_string = os.environ['MONGO_CONNECTION_STRING']
    return get_db(mongo_connection_string)
