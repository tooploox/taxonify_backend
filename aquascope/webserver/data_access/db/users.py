import copy

from aquascope.webserver.data_access.db.db_document import DbDocument

DEFAULT_USERS_PROJECTION = {'_id': 0}


USERS_DB_SCHEMA = {
    'bsonType': 'object',
    'required': ['_id', 'username'],
    #'uniqueItems': ['_id', 'username'],
    'additionalProperties': False,
    'properties': {
        '_id': {
            'bsonType': 'objectId'
        },
        'username': {
            'bsonType': 'string'
        }
    }
}


# class User(DbDocument):
#     def __init__(self, obj):
#         super(User, self).__init__(obj)
#
#     def serializable(self, shallow=False):
#         if shallow:
#             data = self.get_dict()
#         else:
#             data = copy.deepcopy(self.get_dict())
#
#         data['_id'] = str(data['_id'])
#         return data
#
#     @staticmethod
#     def from_db_data(db_data):
#         return User(DbDocument.from_db_data(db_data))


def exists(db, username):
    doc = db.users.count_documents({'username': username}, limit=1)
    return doc is not 0


def list_all(db, with_default_projection=True):
    projection = DEFAULT_USERS_PROJECTION if with_default_projection else None
    return db.users.find({}, projection)


def create(db, username):
    return db.users.insert_one(dict(username=username))
