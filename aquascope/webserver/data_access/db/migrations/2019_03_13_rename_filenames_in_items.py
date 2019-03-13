from pymongo import UpdateOne

from aquascope.webserver.data_access.db.util import get_db_from_env
from aquascope.webserver.data_access.db import items


def rename_filenames_in_items(db):
    # update documents
    filename_phrase_to_delete = '_trand1'
    filename_regex = f'^.*{filename_phrase_to_delete}.*$'
    items_docs = items.find_items(db, filename=filename_regex)

    bulks = []
    for item_doc in items_docs:
        fixed_filename = item_doc.filename.replace(filename_phrase_to_delete, '')
        bulk = UpdateOne({'filename': item_doc.filename}, {'$set': {'filename': fixed_filename}})
        bulks.append(bulk)

    if bulks:
        result = db.items.bulk_write(bulks)
        print(result.bulk_api_result)


def main():
    db = get_db_from_env(with_create_collections=False)
    rename_filenames_in_items(db)


if __name__ == "__main__":
    main()
