from pymongo import UpdateOne

from aquascope.data_processing.upload_postprocess import upload_id_to_item_filenames
from aquascope.webserver.data_access.db import upload
from aquascope.webserver.data_access.db.items import ITEMS_DB_SCHEMA
from aquascope.webserver.data_access.db.util import get_db_from_env, override_collection_validator, \
    get_storage_client_from_env


def add_upload_id_field_to_items(db, storage_client):
    # prepare data for migration
    uploads = upload.find(db, with_default_projection=False)
    duplicates = {}
    for upload_doc in uploads:
        upload_id = upload_doc['_id']
        upload_duplicates = upload_doc.get_dict().get('duplicate_filenames', [])
        duplicates[upload_id] = upload_duplicates

    uploads_filenames = {upload_id: upload_id_to_item_filenames(storage_client, upload_id)
                         for upload_id in duplicates.keys()}

    deduped_ids_and_filenames = []
    for (upload_id, filenames), (_, duplicate_filenames) in zip(uploads_filenames.items(), duplicates.items()):
        deduped_filenames = list(set(filenames) - set(duplicate_filenames))
        deduped_ids_and_filenames += [(upload_id, filename) for filename in deduped_filenames]

    # build queries
    bulks = []
    for upload_id, filename in deduped_ids_and_filenames:
        bulk = UpdateOne({'filename': filename}, {'$set': {'upload_id': upload_id}})
        bulks.append(bulk)

    # set new collection validators
    override_collection_validator(db, 'items', ITEMS_DB_SCHEMA)

    # update DB
    result = db.items.bulk_write(bulks)
    print(result.bulk_api_result)


def main():
    db = get_db_from_env(with_create_collections=False)
    storage_client = get_storage_client_from_env()
    add_upload_id_field_to_items(db, storage_client)


if __name__ == "__main__":
    main()
