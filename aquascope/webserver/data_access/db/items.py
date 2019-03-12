import copy
import os

from bson import ObjectId
import dateutil.parser
from pymongo import UpdateOne

from aquascope.webserver.data_access.db.db_document import DbDocument
from aquascope.webserver.data_access.db.upload import UPLOAD_DB_SCHEMA

TAXONOMY_FIELDS = [
    'empire', 'kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species'
]
ADDITIONAL_ATTRIBUTES_FIELDS = [
    'with_eggs', 'dividing', 'dead', 'with_epibiont', 'with_parasite', 'broken',
    'colony', 'cluster', 'eating', 'multiple_species', 'partially_cropped', 'male',
    'female', 'juvenile', 'adult', 'ephippium', 'resting_egg', 'heterocyst', 'akinete',
    'with_spines', 'beatles', 'stones', 'zeppelin', 'floyd', 'acdc', 'hendrix',
    'alan_parsons', 'allman', 'dire_straits', 'eagles', 'guns', 'purple', 'van_halen',
    'skynyrd', 'zz_top', 'iron', 'police', 'moore', 'inxs', 'chilli_peppers'
]

PRIMARY_MORPHOMETRIC_FIELDS = [
    'file_size', 'aspect_ratio', 'maj_axis_len', 'min_axis_len', 'orientation',
    'eccentricity', 'solidity', 'estimated_volume', 'area'
]

SECONDARY_MORPHOMETRIC_FIELDS = [
    'intensity_gray_mass_displace_in_images', 'intensity_gray_moment_hu_4',
    'intensity_gray_moment_hu_5', 'intensity_gray_moment_hu_6',
    'intensity_gray_moment_hu_7', 'intensity_gray_std_intensity',
    'intensity_gray_moment_hu_1', 'intensity_gray_moment_hu_2',
    'intensity_gray_moment_hu_3', 'intensity_gray_median_intensity',
    'intensity_gray_mass_displace_in_minors', 'intensity_gray_mean_intensity',
    'intensity_gray_perc_25_intensity', 'intensity_gray_perc_75_intensity',
    'intensity_red_mass_displace_in_images', 'intensity_red_moment_hu_4',
    'intensity_red_moment_hu_5', 'intensity_red_moment_hu_6',
    'intensity_red_moment_hu_7', 'intensity_red_std_intensity',
    'intensity_red_moment_hu_1', 'intensity_red_moment_hu_2',
    'intensity_red_moment_hu_3', 'intensity_red_median_intensity',
    'intensity_red_mass_displace_in_minors', 'intensity_red_mean_intensity',
    'intensity_red_perc_25_intensity', 'intensity_red_perc_75_intensity',
    'intensity_green_mass_displace_in_images', 'intensity_green_moment_hu_4',
    'intensity_green_moment_hu_5', 'intensity_green_moment_hu_6',
    'intensity_green_moment_hu_7', 'intensity_green_std_intensity',
    'intensity_green_moment_hu_1', 'intensity_green_moment_hu_2',
    'intensity_green_moment_hu_3', 'intensity_green_median_intensity',
    'intensity_green_mass_displace_in_minors', 'intensity_green_mean_intensity',
    'intensity_green_perc_25_intensity', 'intensity_green_perc_75_intensity',
    'intensity_blue_mass_displace_in_images', 'intensity_blue_moment_hu_4',
    'intensity_blue_moment_hu_5', 'intensity_blue_moment_hu_6',
    'intensity_blue_moment_hu_7', 'intensity_blue_std_intensity',
    'intensity_blue_moment_hu_1', 'intensity_blue_moment_hu_2',
    'intensity_blue_moment_hu_3', 'intensity_blue_median_intensity',
    'intensity_blue_mass_displace_in_minors', 'intensity_blue_mean_intensity',
    'intensity_blue_perc_25_intensity', 'intensity_blue_perc_75_intensity'
]

MORPHOMETRIC_FIELDS = PRIMARY_MORPHOMETRIC_FIELDS + SECONDARY_MORPHOMETRIC_FIELDS

ANNOTABLE_FIELDS = TAXONOMY_FIELDS + ADDITIONAL_ATTRIBUTES_FIELDS

UNNECESSARY_UPLOAD_PROPERTIES = ['state', 'image_count', 'duplicate_image_count', 'duplicate_filenames']
NO_UNNECESSARY_UPLOAD_PROPERTIES_PROJECTION = {k: 0 for k in UNNECESSARY_UPLOAD_PROPERTIES}

DEFAULT_ITEM_PROJECTION = {
    **NO_UNNECESSARY_UPLOAD_PROPERTIES_PROJECTION,
    **{k: 0 for k in SECONDARY_MORPHOMETRIC_FIELDS}
}

ITEMS_DB_SCHEMA = {
    'bsonType': 'object',
    'required': ['_id', 'upload_id', 'filename', 'extension', 'group_id',
                 'acquisition_time', 'image_width', 'image_height']
                + TAXONOMY_FIELDS
                + ADDITIONAL_ATTRIBUTES_FIELDS
                + MORPHOMETRIC_FIELDS
                + [f'{k}_modified_by' for k in ANNOTABLE_FIELDS]
                + [f'{k}_modification_time' for k in ANNOTABLE_FIELDS],
    'additionalProperties': False,
    'properties': {
        '_id': {
            'bsonType': 'objectId'
        },
        'upload_id': {
            'bsonType': 'objectId'
        },
        'filename': {
            'bsonType': 'string'
        },
        'extension': {
            'bsonType': 'string'
        },
        'group_id': {
            'bsonType': 'string'
        },
        'acquisition_time': {
            'bsonType': 'date'
        },
        'image_width': {
            'bsonType': 'int'
        },
        'image_height': {
            'bsonType': 'int'
        },
        **({k: dict(bsonType=['string', 'null']) for k in TAXONOMY_FIELDS}),
        **({k: dict(bsonType=['bool', 'null']) for k in ADDITIONAL_ATTRIBUTES_FIELDS}),
        **({k: dict(bsonType='double') for k in MORPHOMETRIC_FIELDS}),
        **({f'{k}_modified_by': dict(bsonType=['string', 'null']) for k in ANNOTABLE_FIELDS}),
        **({f'{k}_modification_time': dict(bsonType=['date', 'null']) for k in ANNOTABLE_FIELDS})
    }
}


def make_item_dict_serializable(item_dict):
    for field in ANNOTABLE_FIELDS:
        date_field = f'{field}_modification_time'
        if item_dict[date_field]:
            item_dict[date_field] = item_dict[date_field].isoformat()

    item_dict['acquisition_time'] = item_dict['acquisition_time'].isoformat()
    item_dict['_id'] = str(item_dict['_id'])
    item_dict['upload_id'] = str(item_dict['upload_id'])
    return item_dict


class Item(DbDocument):
    def __init__(self, obj):
        super(Item, self).__init__(obj)

    @staticmethod
    def from_request(request_dict):
        data = copy.deepcopy(request_dict)
        data['_id'] = ObjectId(data['_id'])
        data['upload_id'] = ObjectId(data['upload_id'])
        data.pop('tags', None)
        return Item(data)

    @staticmethod
    def from_db_data(db_data):
        return Item(DbDocument.from_db_data(db_data))

    @staticmethod
    def from_tsv_row(row, image_width, image_height, upload_id):
        item = copy.deepcopy(row)
        item['acquisition_time'] = item.pop('timestamp').to_pydatetime()
        item['filename'] = os.path.basename(item.pop('url'))
        item['image_width'] = image_width
        item['image_height'] = image_height
        item['extension'] = os.path.splitext(item['filename'])[1]
        item['group_id'] = 'processed'
        item['upload_id'] = ObjectId(upload_id)
        return Item(item)

    def serializable(self, shallow=False):
        if shallow:
            data = self.get_dict()
        else:
            data = copy.deepcopy(self.get_dict())

        return make_item_dict_serializable(data)


def add_user_and_modification_times_to_query(query, user, modification_time_start,
                                             modification_time_end):
    # are there any annotable fields in the query?
    any_annotable_fields = any(key in ANNOTABLE_FIELDS for key in query.keys())

    if any_annotable_fields:
        for key in list(query.keys()):
            if key in ANNOTABLE_FIELDS:
                if user or user == '':
                    query[f'{key}_modified_by'] = None if user == '' else user

                modification_time_key = f'{key}_modification_time'
                if modification_time_start:
                    if modification_time_key not in query:
                        query[modification_time_key] = {}
                    query[modification_time_key]['$gte'] = modification_time_start
                if modification_time_end:
                    if modification_time_key not in query:
                        query[modification_time_key] = {}
                    query[modification_time_key]['$lt'] = modification_time_end

    else:
        date_or_alternatives = []
        user_or_alternatives = []
        for key in ANNOTABLE_FIELDS:
            if user or user == '':
                user_or_alternatives.append({
                    f'{key}_modified_by': None if user == '' else user
                })

            modification_time_key = f'{key}_modification_time'
            time_range_query = {}
            if modification_time_start:
                time_range_query['$gte'] = modification_time_start
            if modification_time_end:
                time_range_query['$lt'] = modification_time_end

            if modification_time_start or modification_time_end:
                date_or_alternatives.append({
                    modification_time_key: time_range_query
                })

        if date_or_alternatives and user_or_alternatives:
            query['$and'] = [
                {'$or': date_or_alternatives},
                {'$or': user_or_alternatives}
            ]
        elif date_or_alternatives:
            query['$or'] = date_or_alternatives
        elif user_or_alternatives:
            query['$or'] = user_or_alternatives

    return query


def build_find_query(*args, **kwargs):
    modified_by = kwargs.pop('modified_by', None)
    modification_time_start = kwargs.pop('modification_time_start', None)
    modification_time_end = kwargs.pop('modification_time_end', None)

    query = dict()
    for key, value in kwargs.items():
        if key == 'tags':
            if value:
                query['tags'] = {
                    '$all': value
                }
            else:
                query['tags'] = value
        elif type(value) == list:
            query[key] = {
                '$in': value
            }
        elif key == 'filename':
            query[key] = {
                '$regex': value
            }
        elif key == 'acquisition_time_start':
            if 'acquisition_time' not in query:
                query['acquisition_time'] = {}

            query['acquisition_time']['$gte'] = value
        elif key == 'acquisition_time_end':
            if 'acquisition_time' not in query:
                query['acquisition_time'] = {}

            query['acquisition_time']['$lt'] = value
        else:
            query[key] = value

    query = add_user_and_modification_times_to_query(query, modified_by, modification_time_start, modification_time_end)
    return query


def format_query_result(result, serializable):
    if serializable:
        return (make_item_dict_serializable(item) for item in result)

    return (Item.from_db_data(item) for item in result)


def aggregate_find_query(query, projection, skip=None, limit=None):
    aggregate_query = [
        {
            '$lookup': {
                'from': 'uploads',
                'localField': 'upload_id',
                'foreignField': '_id',
                'as': 'from_upload'
            }
        },
        {
            '$replaceRoot': {
                'newRoot': {
                    '$mergeObjects': [{
                        '$arrayElemAt': ["$from_upload", 0]}, "$$ROOT"]
                }
            }
        },
        {
            '$match': query
        },
        {
            '$project': {
                'from_upload': 0
            }
        },
        {
            '$project': projection
        }
    ]
    if skip:
        aggregate_query.append({
            '$skip': skip
        })
    if limit:
        aggregate_query.append({
            '$limit': limit
        })

    return aggregate_query


def paged_find_items(db, page_number, page_size, with_default_projection=True,
                     serializable=False, *args, **kwargs):
    query = build_find_query(*args, **kwargs)
    projection = DEFAULT_ITEM_PROJECTION if with_default_projection else NO_UNNECESSARY_UPLOAD_PROPERTIES_PROJECTION
    skip = page_size * (page_number - 1)
    limit = page_size
    result = db.items.aggregate(aggregate_find_query(query, projection, skip, limit))
    return format_query_result(result, serializable)


def find_items(db, with_default_projection=True, serializable=False, *args, **kwargs):
    query = build_find_query(*args, **kwargs)
    projection = DEFAULT_ITEM_PROJECTION if with_default_projection else NO_UNNECESSARY_UPLOAD_PROPERTIES_PROJECTION
    result = db.items.aggregate(aggregate_find_query(query, projection))
    return format_query_result(result, serializable)


def bulk_replace(db, items):
    bulks = []
    for current, update in items:
        bulk = UpdateOne(current.get_dict(), {'$set': update.get_dict()})
        bulks.append(bulk)

    return db.items.bulk_write(bulks)
