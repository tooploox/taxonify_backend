from bson import ObjectId

from aquascope.webserver.data_access.db.upload import Upload

DUMMY_UPLOADS = [
    Upload({
        '_id': ObjectId('000000000000000000001000'),
        'filename': 'dummy0',
        'state': 'initialized'
    }),
    Upload({
        '_id': ObjectId('000000000000000000001001'),
        'filename': 'dummy1',
        'state': 'processing'
    }),
    Upload({
        '_id': ObjectId('000000000000000000001002'),
        'filename': 'dummy2',
        'state': 'finished'
    }),
    Upload({
        '_id': ObjectId('000000000000000000001003'),
        'filename': 'dummy3',
        'state': 'failed'
    })
]
