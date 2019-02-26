from aquascope.webserver.data_access.db.items import ANNOTABLE_FIELDS, ITEMS_DB_SCHEMA
from aquascope.webserver.data_access.db.util import get_db_from_env, override_collection_validator


def add_modification_fields_to_item_schema(db):
    # set new collection validators
    override_collection_validator(db, 'items', ITEMS_DB_SCHEMA)

    # update documents
    db.items.update_many({}, {
        '$set': {
            **({f'{k}_modified_by': None for k in ANNOTABLE_FIELDS}),
            **({f'{k}_modification_time': None for k in ANNOTABLE_FIELDS})
        }
    })


def main():
    db = get_db_from_env(with_create_collections=False)
    add_modification_fields_to_item_schema(db)


if __name__ == "__main__":
    main()
