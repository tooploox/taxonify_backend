import unittest
from unittest import mock

import dateutil
from azure.storage.blob.blockblobservice import BlockBlobService
from bson import ObjectId
from flask import current_app as app
import mongomock

from aquascope.webserver.app import make_app
from aquascope.webserver.data_access.util import populate_db_with_items
from aquascope.tests.aquascope.webserver.data_access.db.dummy_items import DUMMY_ITEMS
from aquascope.webserver.data_access.db.items import find_items

MONGO_CONNECTION_STRING = 'mongodb://example.server.com/aquascopedb'


class TestFindItems(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        client = mongomock.MongoClient(MONGO_CONNECTION_STRING)
        cls.db = client.get_database()
        with mock.patch.object(BlockBlobService, '__init__', lambda x, connection_string: None):
            cls.app = make_app(cls.db, '', '', '', '',
                               environment='TESTING', celery_user='',
                               celery_password='', celery_address='')

    def setUp(self):
        with self.app.app_context():
            self.test_app = app.test_client()
            populate_db_with_items(DUMMY_ITEMS, self.db)

    def tearDown(self):
        with self.app.app_context():
            db = self.app.config['db']
            db.items.drop()

    def test_bool_nullable_field_with_bool(self):
        with self.app.app_context():
            find_query = {
                'eating': ['True']
            }
            res = list(find_items(**find_query))
            res = [res['_id'] for res in res]
            expected = [
                ObjectId('000000000000000000000000'),
                ObjectId('000000000000000000000001')
            ]
            self.assertCountEqual(res, expected)

    def test_bool_nullable_field_with_none(self):
        with self.app.app_context():
            find_query = {
                'eating': ['']
            }
            res = list(find_items(**find_query))
            res = [res['_id'] for res in res]
            expected = [
                ObjectId('000000000000000000000003'),
                ObjectId('000000000000000000000004')
            ]
            self.assertCountEqual(res, expected)

    def test_bool_nullable_field_with_bool_and_none(self):
        with self.app.app_context():
            find_query = {
                'eating': ['True', '']
            }
            res = list(find_items(**find_query))
            res = [res['_id'] for res in res]
            expected = [
                ObjectId('000000000000000000000000'),
                ObjectId('000000000000000000000001'),
                ObjectId('000000000000000000000003'),
                ObjectId('000000000000000000000004')
            ]
            self.assertCountEqual(res, expected)

    def test_datetime_field(self):
        with self.app.app_context():
            find_query = {
                'acquisition_time_start': dateutil.parser.parse('2019-01-11T18:06:34.151Z')
            }
            res = list(find_items(**find_query))
            res = [res['_id'] for res in res]
            expected = [
                ObjectId('000000000000000000000000'),
                ObjectId('000000000000000000000001')
            ]
            self.assertCountEqual(res, expected)

    def test_datetime_fields_range(self):
        with self.app.app_context():
            find_query = {
                'acquisition_time_start': dateutil.parser.parse('2019-01-02T18:06:34.151Z'),
                'acquisition_time_end': dateutil.parser.parse('2019-01-11T18:06:34.151Z')
            }
            res = list(find_items(**find_query))
            res = [res['_id'] for res in res]
            expected = [
                ObjectId('000000000000000000000003'),
                ObjectId('000000000000000000000002')
            ]
            self.assertCountEqual(res, expected)

    def test_fields_combination(self):
        with self.app.app_context():
            find_query = {
                'species': 'sp',
                'dead': ['True', 'False'],
                'acquisition_time_end': dateutil.parser.parse('2019-01-15T18:06:34.151Z')
            }
            res = list(find_items(**find_query))
            res = [res['_id'] for res in res]
            expected = [
                ObjectId('000000000000000000000002')
            ]
            self.assertCountEqual(res, expected)


if __name__ == '__main__':
    unittest.main()
