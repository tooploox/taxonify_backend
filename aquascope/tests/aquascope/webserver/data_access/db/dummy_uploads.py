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
        'state': 'uploaded'
    }),
    Upload({
        '_id': ObjectId('000000000000000000001002'),
        'filename': 'dummy2',
        'state': 'processing',
        'image_count': 20,
        'duplicate_image_count': 0,
        'duplicate_filenames': []
    }),
    Upload({
        '_id': ObjectId('000000000000000000001003'),
        'filename': 'dummy3',
        'state': 'finished',
        'image_count': 10,
        'duplicate_image_count': 2,
        'duplicate_filenames': [
            'img1.jpg',
            'img2.jpg'
        ]
    }),
    Upload({
        '_id': ObjectId('000000000000000000001004'),
        'filename': 'dummy4',
        'state': 'failed'
    })
]
