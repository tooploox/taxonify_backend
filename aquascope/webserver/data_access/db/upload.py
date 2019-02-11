import copy

from bson import ObjectId

from aquascope.webserver.data_access.db.db_document import DbDocument


class Upload(DbDocument):
    def __init__(self, obj):
        super(Upload, self).__init__(obj)

    def serializable(self):
        data = self.get_dict()
        data['generation_date'] = data['_id'].generation_time.isoformat()
        data['_id'] = str(data['_id'])
        return data

    @staticmethod
    def from_db_data(db_data):
        return Upload(copy.deepcopy(db_data))


def create(db, filename):
    return db.uploads.insert_one(dict(filename=filename, state='initialized'))


def get(db, document_id):
    doc = db.uploads.find_one({'_id': ObjectId(document_id)})
    return Upload.from_db_data(doc)


def find(db, query_filter=None):
    if not query_filter:
        query_filter = {}

    return (Upload.from_db_data(doc) for doc in db.uploads.find(query_filter))


def update_state(db, document_id, state):
    return db.uploads.update_one({'_id': ObjectId(document_id)}, {'$set': {'state': state}})
