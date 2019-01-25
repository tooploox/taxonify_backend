import dateutil.parser
from bson import ObjectId

from aquascope.webserver.data_access.db import Item

DUMMY_ITEMS = [
    Item({
        '_id': ObjectId('000000000000000000000000'),
        'filename': 'image_000.jpeg',
        'extension': '.jpeg',
        'group_id': 'processed',
        'empire': 'prokaryota',
        'kingdom': 'Bacteria',
        'phylum': 'Cyanobacteria',
        'class': 'Cyanophyceae',
        'order': 'Nostocales',
        'family': 'Nostocaceae',
        'genus': 'Anabaena',
        'species': 'sp',
        'dividing': False,
        'dead': False,
        'with_epiphytes': False,
        'broken': False,
        'colony': False,
        'eating': True,
        'multiple_species': False,
        'cropped': False,
        'male': None,
        'female': None,
        'juvenile': None,
        'adult': None,
        'with_eggs': None,
        'acquisition_time': dateutil.parser.parse('2019-01-20 10:00:00.000Z'),
        'image_width': 100,
        'image_height': 100
    }),
    Item({
        '_id': ObjectId('000000000000000000000001'),
        'filename': 'image_001.jpeg',
        'extension': '.jpeg',
        'group_id': 'processed',
        'empire': 'prokaryota',
        'kingdom': 'Bacteria',
        'phylum': 'Cyanobacteria',
        'class': 'Cyanophyceae',
        'order': 'Nostocales',
        'family': 'Nostocaceae',
        'genus': 'Anabaena',
        'species': 'sp',
        'dividing': False,
        'dead': False,
        'with_epiphytes': False,
        'broken': False,
        'colony': False,
        'eating': True,
        'multiple_species': False,
        'cropped': False,
        'male': None,
        'female': False,
        'juvenile': None,
        'adult': None,
        'with_eggs': None,
        'acquisition_time': dateutil.parser.parse('2019-01-20 06:00:00.000Z'),
        'image_width': 100,
        'image_height': 100
    }),
    Item({
        '_id': ObjectId('000000000000000000000002'),
        'filename': 'image_002.jpeg',
        'extension': '.jpeg',
        'group_id': 'processed',
        'empire': 'prokaryota',
        'kingdom': 'Bacteria',
        'phylum': 'Cyanobacteria',
        'class': 'Cyanophyceae',
        'order': 'Nostocales',
        'family': 'Nostocaceae',
        'genus': 'Anabaena',
        'species': 'sp',
        'dividing': False,
        'dead': False,
        'with_epiphytes': False,
        'broken': False,
        'colony': False,
        'eating': False,
        'multiple_species': False,
        'cropped': False,
        'male': None,
        'female': True,
        'juvenile': None,
        'adult': None,
        'with_eggs': None,
        'acquisition_time': dateutil.parser.parse('2019-01-10 10:00:00.000Z'),
        'image_width': 100,
        'image_height': 100
    }),
    Item({
        '_id': ObjectId('000000000000000000000003'),
        'filename': 'image_003.jpeg',
        'extension': '.jpeg',
        'group_id': 'processed',
        'empire': 'prokaryota',
        'kingdom': 'Bacteria',
        'phylum': 'Cyanobacteria',
        'class': 'Cyanophyceae',
        'order': 'Sphaeropleales',
        'family': 'Scenedesmaceae',
        'genus': 'Coelastrum',
        'species': 'reticulatum',
        'dividing': False,
        'dead': False,
        'with_epiphytes': False,
        'broken': False,
        'colony': False,
        'eating': None,
        'multiple_species': False,
        'cropped': False,
        'male': None,
        'female': None,
        'juvenile': None,
        'adult': None,
        'with_eggs': None,
        'acquisition_time': dateutil.parser.parse('2019-01-05 10:00:00.000Z'),
        'image_width': 100,
        'image_height': 100
    }),
    Item({
        '_id': ObjectId('000000000000000000000004'),
        'filename': 'image_004.jpeg',
        'extension': '.jpeg',
        'group_id': 'processed',
        'empire': 'prokaryota',
        'kingdom': 'Bacteria',
        'phylum': 'Cyanobacteria',
        'class': 'Cyanophyceae',
        'order': 'Sphaeropleales',
        'family': 'Scenedesmaceae',
        'genus': 'Coelastrum',
        'species': 'reticulatum',
        'dividing': False,
        'dead': False,
        'with_epiphytes': False,
        'broken': False,
        'colony': False,
        'eating': None,
        'multiple_species': False,
        'cropped': False,
        'male': None,
        'female': None,
        'juvenile': None,
        'adult': None,
        'with_eggs': None,
        'acquisition_time': dateutil.parser.parse('2019-01-01 10:00:00.000Z'),
        'image_width': 100,
        'image_height': 100
    })
]
