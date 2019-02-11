from bson import ObjectId


def create(db, filename):
    return db.uploads.insert_one(dict(filename=filename, state='initialized'))


def get(db, document_id):
    return db.uploads.find_one({'_id': ObjectId(document_id)})


def update_state(db, document_id, state):
    return db.uploads.update_one({'_id': ObjectId(document_id)}, {'$set': {'state': state}})
