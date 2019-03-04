import copy

from pymongo import UpdateOne

from aquascope.webserver.data_access.db.items import ANNOTABLE_FIELDS
from aquascope.webserver.data_access.db.util import get_db_from_env


def set_marta_to_modified_by_in_not_null_annotable_fields(db):

    # get all items that have any annotable field annotated and corresponding _modified_by set to None
    ors = []
    for field in ANNOTABLE_FIELDS:
        ors.append({
            field: {'$ne': None},
            f'{field}_modified_by': None
        })
    items = db.items.find({'$or': ors})

    # set _modified_by fields to 'marta.reyes' for all annotated annotable fields
    bulks = []
    for item in items:
        update = copy.deepcopy(item)

        for field in ANNOTABLE_FIELDS:
            if update[field] is not None and update[f'{field}_modified_by'] is None:
                update[f'{field}_modified_by'] = 'marta.reyes'
        bulk = UpdateOne(item, {'$set': update})
        bulks.append(bulk)

    if bulks:
        db.items.bulk_write(bulks)


def main():
    db = get_db_from_env(with_create_collections=False)
    set_marta_to_modified_by_in_not_null_annotable_fields(db)


if __name__ == "__main__":
    main()
