import os

from pymongo import MongoClient
from pymongo.errors import CollectionInvalid

from aquascope.webserver.data_access.db.items import ITEMS_DB_SCHEMA
from aquascope.webserver.data_access.db.upload import UPLOAD_DB_SCHEMA


def create_collections(db):
    try:
        db.create_collection('items', validator={'$jsonSchema': ITEMS_DB_SCHEMA})
        db.create_collection('uploads', validator={'$jsonSchema': UPLOAD_DB_SCHEMA})
    except CollectionInvalid:
        pass


def get_db(connection_string):
    mongo_client = MongoClient(connection_string)
    db = mongo_client.get_database()
    create_collections(db)
    return db


def get_db_from_env():
    mongo_connection_string = os.environ['MONGO_CONNECTION_STRING']
    return get_db(mongo_connection_string)
