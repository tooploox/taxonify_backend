from datetime import datetime
import copy

from bson import ObjectId
from flask import current_app as app
from flask_restful import inputs
from pymongo import ReplaceOne
import dateutil.parser


class ItemInitializationError(ValueError):
    pass


class Item:
    def __init__(self, request_dict=None, db_data=None, csv_row=None):
        if request_dict is None and db_data is None and csv_row is None:
            raise ItemInitializationError("Item object has to be initialized either with"
                                          "request dict or with db object or with csv_row")
        if request_dict:
            self.data = request_dict
            self.data['_id'] = ObjectId(self.data['_id'])
            self.data['acquisition_time'] = dateutil.parser.parse(self.data['acquisition_time'])
        elif db_data:
            self.data = db_data
        elif csv_row:
            def remap_values(key, value):
                if value == 'FALSE':
                    value = False
                elif value == 'TRUE':
                    value = True
                elif value == 'null':
                    value = None
                elif key == 'acquisition_time':
                    value = float(value)
                    value = datetime.fromtimestamp(value)
                elif key == 'image_width' or key == 'image_height':
                    value = int(value)
                return value

            self.data = {k: remap_values(k, v) for k, v in csv_row.items()}

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
        else:
            value = remap_value(value)
            query[key] = value

    db = app.config['db']
    return (Item(db_data=item) for item in db.items.find(query))


def bulk_replace(items):
    bulks = []
    for current, update in items:
        bulk = ReplaceOne(current.get_dict(), update.get_dict())
        bulks.append(bulk)

    db = app.config['db']
    return db.items.bulk_write(bulks)
