from aquascope.webserver.data_access.db.upload import UPLOAD_DB_SCHEMA
from aquascope.webserver.data_access.db.util import get_db_from_env, override_collection_validator


def add_tags_field_to_uploads(db):
    # set new collection validators
    override_collection_validator(db, 'uploads', UPLOAD_DB_SCHEMA)

    # update documents
    db.uploads.update_many({}, {
        '$set': {'tags': []}
    })


def main():
    db = get_db_from_env(with_create_collections=False)
    add_tags_field_to_uploads(db)


if __name__ == "__main__":
    main()
