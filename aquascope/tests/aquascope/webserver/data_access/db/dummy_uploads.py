import copy

from bson import ObjectId

from aquascope.webserver.data_access.db.upload import Upload, DEFAULT_UPLOAD_PROJECTION
from aquascope.webserver.data_access.db.util import project_dict

_DUMMY_UPLOADS = [
    {
        '_id': ObjectId('000000000000000000001000'),
        'filename': 'dummy0',
        'state': 'initialized',
        'tags': []
    },
    {
        '_id': ObjectId('000000000000000000001001'),
        'filename': 'dummy1',
        'state': 'uploaded',
        'tags': []
    },
    {
        '_id': ObjectId('000000000000000000001002'),
        'filename': 'dummy2',
        'state': 'processing',
        'image_count': 20,
        'duplicate_image_count': 0,
        'duplicate_filenames': [],
        'tags': []
    },
    {
        '_id': ObjectId('000000000000000000001003'),
        'filename': 'dummy3',
        'state': 'finished',
        'image_count': 10,
        'duplicate_image_count': 2,
        'duplicate_filenames': [
            'img1.jpg',
            'img2.jpg'
        ],
        'tags': []
    },
    {
        '_id': ObjectId('000000000000000000001004'),
        'filename': 'dummy4',
        'state': 'failed',
        'tags': []
    }
]

DUMMY_UPLOADS_WITH_DEFAULT_PROJECTION = [
    Upload(project_dict(copy.deepcopy(upload), DEFAULT_UPLOAD_PROJECTION)) for upload in _DUMMY_UPLOADS
]

DUMMY_UPLOADS = [Upload(upload) for upload in _DUMMY_UPLOADS]
