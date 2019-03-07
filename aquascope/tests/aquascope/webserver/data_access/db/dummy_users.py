import copy

from bson import ObjectId

from aquascope.webserver.data_access.db.users import DEFAULT_USERS_PROJECTION
from aquascope.webserver.data_access.db.util import project_dict

DUMMY_USERS = [
    {
        '_id': ObjectId('000000000000000000010000'),
        'username': 'user0'
     },
    {
        '_id': ObjectId('000000000000000000010001'),
        'username': 'user1'
    }
]

DUMMY_USERS_WITH_DEFAULT_PROJECTION = [
    project_dict(copy.deepcopy(user), DEFAULT_USERS_PROJECTION) for user in DUMMY_USERS
]
