import copy

from bson import ObjectId

from aquascope.webserver.data_access.db.db_document import DbDocument

UPLOAD_DB_SCHEMA = {
    'bsonType': 'object',
    'required': ['_id', 'filename', 'state', 'tags'],
    'additionalProperties': False,
    'properties': {
        '_id': {
            'bsonType': 'objectId'
        },
        'filename': {
            'bsonType': 'string'
        },
        'state': {
            'bsonType': 'string',
            'enum': ['initialized', 'uploaded', 'processing', 'finished', 'failed']
        },
        'tags': {
            'bsonType': 'array',
            'items': {
                'bsonType': 'string',
                'uniqueItems': True
            }
        },
        'image_count': {
            'bsonType': 'int'
        },
        'duplicate_image_count': {
            'bsonType': 'int'
        },
        'duplicate_filenames': {
            'bsonType': 'array',
            'items': {
                'bsonType': 'string'
            }
        },
        'broken_record_count': {
            'bsonType': 'int'
        },
        'broken_records': {
            'bsonType': 'array',
            'items': {
                'bsonType': 'string'
            }
        }
    }
}

DEFAULT_UPLOAD_PROJECTION = {'duplicate_filenames': 0}


class Upload(DbDocument):
    def __init__(self, obj):
        super(Upload, self).__init__(obj)

    def serializable(self, shallow=False):
        if shallow:
            data = self.get_dict()
        else:
            data = copy.deepcopy(self.get_dict())

        data['generation_date'] = data['_id'].generation_time.isoformat()
        data['_id'] = str(data['_id'])
        return data

    @staticmethod
    def from_db_data(db_data):
        return Upload(DbDocument.from_db_data(db_data))


def create(db, filename):
    return db.uploads.insert_one(dict(filename=filename, state='initialized', tags=[]))


def get(db, document_id, with_default_projection=True):
    projection = DEFAULT_UPLOAD_PROJECTION if with_default_projection else None
    doc = db.uploads.find_one({'_id': ObjectId(document_id)}, projection)
    return Upload.from_db_data(doc) if doc else None


def find(db, query_filter=None, with_default_projection=True):
    projection = DEFAULT_UPLOAD_PROJECTION if with_default_projection else None
    if not query_filter:
        query_filter = {}

    return (Upload.from_db_data(doc) for doc in db.uploads.find(query_filter, projection))


def update_state(db, document_id, state, **kwargs):
    return db.uploads.update_one({'_id': ObjectId(document_id)}, {'$set': {'state': state, **kwargs}})


def update_tags(db_client, db, document_id, tags):
    with db_client.start_session() as session:
        res = db.uploads.update_one({'_id': ObjectId(document_id), 'state': 'finished'},
                                    {'$set': {'tags': tags}}, session=session)

        db.items.update_many({'upload_id': ObjectId(document_id)},
                             {'$set': {'tags': tags}}, session=session)

        return res


def get_tags(db, document_id):
    return db.uploads.find_one({'_id': document_id}, {'tags': 1})['tags']
