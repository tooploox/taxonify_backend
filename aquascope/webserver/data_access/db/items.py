import copy

from bson import ObjectId
import dateutil.parser
from flask import current_app as app
from flask_restful import inputs
from pymongo import ReplaceOne


class ItemInitializationError(ValueError):
    pass


class Item:
    def __init__(self, data):
        self.data = data

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
        data = copy.deepcopy(self.data)
        data['acquisition_time'] = data['acquisition_time'].isoformat()
        data['_id'] = str(data['_id'])
        return data

    def get_dict(self):
        return self.data

    def __getitem__(self, key):
        return self.data[key]

    def __getattr__(self, k):
        try:
            v = self.data[k]
        except KeyError:
            raise AttributeError(k)

        return v


def remap_value(value):
    if value == '':
        value = None
    else:
        try:
            value = inputs.boolean(value)
        except ValueError:
            pass

    return value


def find_items(*args, **kwargs):
    query = dict()
    for key, value in kwargs.items():
        if type(value) == list:
            value = [remap_value(val) for val in value]
            query[key] = {
                '$in': value
            }
        elif key == 'filename':
            query[key] = {
                '$regex': value
            }
        else:
            value = remap_value(value)
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
