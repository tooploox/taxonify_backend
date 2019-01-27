from schema import Schema, Or


post_item_schema = Schema({
    '_id': str,
    'filename': str,
    'extension': str,
    'group_id': str,

    'empire': str,
    'kingdom': str,
    'phylum': str,
    'class': str,
    'order': str,
    'family': str,
    'genus': str,
    'species': str,

    'eating': Or(bool, None),
    'dividing': Or(bool, None),
    'dead': Or(bool, None),
    'with_epiphytes': Or(bool, None),
    'broken': Or(bool, None),
    'colony': Or(bool, None),
    'multiple_species': Or(bool, None),
    'cropped': Or(bool, None),
    'male': Or(bool, None),
    'female': Or(bool, None),
    'juvenile': Or(bool, None),
    'adult': Or(bool, None),
    'with_eggs': Or(bool, None),

    'acquisition_time': str,
    'image_width': int,
    'image_height': int
})
post_items_update_schema = Schema([
    {
        'current': post_item_schema,
        'update': post_item_schema
    }
])
