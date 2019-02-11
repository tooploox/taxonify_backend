import copy

from bson import ObjectId
import dateutil.parser
from pymongo import ReplaceOne

from aquascope.webserver.data_access.db.db_document import DbDocument


class Item(DbDocument):
    def __init__(self, obj):
        super(Item, self).__init__(obj)

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


def find_items(db, *args, **kwargs):
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

    return (Item.from_db_data(item) for item in db.items.find(query))


def bulk_replace(db, items):
    bulks = []
    for current, update in items:
        bulk = ReplaceOne(current.get_dict(), update.get_dict())
        bulks.append(bulk)

    return db.items.bulk_write(bulks)
