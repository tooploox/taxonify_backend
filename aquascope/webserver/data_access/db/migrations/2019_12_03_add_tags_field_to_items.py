from bson import ObjectId
from pymongo import UpdateMany

from aquascope.webserver.data_access.db import upload
from aquascope.webserver.data_access.db.items import ITEMS_DB_SCHEMA
from aquascope.webserver.data_access.db.util import get_db_from_env, get_storage_client_from_env, \
    override_collection_validator


def add_tags_field_to_items(db):
    uploads = upload.find(db, with_default_projection=False)

    # build query
    bulks = []
    for upload_doc in uploads:
        upload_id = upload_doc['_id']
        upload_tags = upload_doc['tags']

        bulk = UpdateMany({'upload_id': ObjectId(upload_id)},
                          {'$set': {'tags': upload_tags}})
        bulks.append(bulk)

    # set new collection validators
    override_collection_validator(db, 'items', ITEMS_DB_SCHEMA)

    if bulks:
        # update DB
        result = db.items.bulk_write(bulks)
        print(result.bulk_api_result)


def main():
    db_client, db = get_db_from_env(with_create_collections=False)
    add_tags_field_to_items(db)


if __name__ == "__main__":
    main()
