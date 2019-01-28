import copy

from bson import ObjectId
import dateutil.parser
from flask import current_app as app
from flask_restful import inputs
from pymongo import ReplaceOne


class ItemInitializationError(ValueError):
    pass


class Item(object):
    def __init__(self, obj):
        for k, v in obj.items():
            if isinstance(v, dict):
                setattr(self, k, Item(v))
            else:
                setattr(self, k, v)

    def __getitem__(self, key):
        return self.__dict__[key]

    def __repr__(self):
        return '{%s}' % str(', '.join('%s : %s' % (k, repr(v)) for
                                      (k, v) in self.__dict__.items()))

    @staticmethod
    def from_request(request_dict):
        data = copy.deepcopy(request_dict)
        data['_id'] = ObjectId(data['_id'])
        data['acquisition_time'] = dateutil.parser.parse(data['acquisition_time'])
        return Item(data)

    @staticmethod
    def from_db_data(db_data):
        return Item(copy.deepcopy(db_data))

    def serializable(self):
        data = self.get_dict()
        data['acquisition_time'] = data['acquisition_time'].isoformat()
        data['_id'] = str(data['_id'])
        return data

    def get_dict(self):
        return copy.deepcopy(self.__dict__)


def find_items(*args, **kwargs):
    query = dict()
    for key, value in kwargs.items():
        if type(value) == list:
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

    db = app.config['db']
    return (Item.from_db_data(item) for item in db.items.find(query))


def bulk_replace(items):
    bulks = []
    for current, update in items:
        bulk = ReplaceOne(current.get_dict(), update.get_dict())
        bulks.append(bulk)

    db = app.config['db']
    return db.items.bulk_write(bulks)
