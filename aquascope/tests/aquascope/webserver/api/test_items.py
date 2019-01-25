import unittest
from unittest import mock

from azure.storage.blob import BlockBlobService
from flask import current_app as app, url_for
import mongomock
from flask_jwt_extended import create_access_token

from aquascope.tests.aquascope.webserver.data_access.db.dummy_items import DUMMY_ITEMS
from aquascope.webserver.app import make_app
from aquascope.webserver.data_access.util import populate_db_with_items

MONGO_CONNECTION_STRING = 'mongodb://example.server.com/aquascopedb'


class TestItems(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        client = mongomock.MongoClient(MONGO_CONNECTION_STRING)
        cls.db = client.get_database()
        with mock.patch.object(BlockBlobService, '__init__', lambda x, connection_string: None):
            cls.app = make_app(cls.db, '', 'jwtdummysecret', '', '',
                               environment='TESTING', celery_user='',
                               celery_password='', celery_address='')

    def setUp(self):
        with self.app.app_context():
            self.client = app.test_client
            populate_db_with_items(DUMMY_ITEMS, self.db)

            access_token = create_access_token('testuser')
            self.headers = {
                'Authorization': 'Bearer {}'.format(access_token)
            }

    def tearDown(self):
        with self.app.app_context():
            db = self.app.config['db']
            db.items.drop()

    @mock.patch('aquascope.webserver.data_access.storage.blob.make_blob_url')
    def test_api_can_get_items_by_eating(self, mock_make_blob_url):
        mock_make_blob_url.return_value = 'mockedurl'
        with self.app.app_context():
            request_data = {
                'eating': True
            }
            res = self.client().get('/items', query_string=request_data, headers=self.headers)
            self.assertEqual(res.status_code, 200)

            response = res.json
            expected_items = [DUMMY_ITEMS[0], DUMMY_ITEMS[1]]
            expected_items = [item.serializable() for item in expected_items]

            self.assertEqual(response['items'], expected_items)

    @mock.patch('aquascope.webserver.data_access.storage.blob.make_blob_url')
    def test_api_can_get_items_by_eating_list(self, mock_make_blob_url):
        mock_make_blob_url.return_value = 'mockedurl'
        with self.app.app_context():
            request_data = {
                'eating': [True, '']
            }
            res = self.client().get('/items', query_string=request_data, headers=self.headers)
            self.assertEqual(res.status_code, 200)

            response = res.json
            expected_items = [DUMMY_ITEMS[0], DUMMY_ITEMS[1], DUMMY_ITEMS[3], DUMMY_ITEMS[4]]
            expected_items = [item.serializable() for item in expected_items]

            self.assertEqual(response['items'], expected_items)
