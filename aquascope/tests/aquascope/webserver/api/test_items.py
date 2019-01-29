import copy
import unittest
from unittest import mock

from flask import json

from aquascope.tests.aquascope.webserver.data_access.db.dummy_items import DUMMY_ITEMS
from aquascope.tests.flask_app_test_case import FlaskAppTestCase
from aquascope.webserver.data_access.db import Item

MONGO_CONNECTION_STRING = 'mongodb://example.server.com/aquascopedb'


class TestGetItems(FlaskAppTestCase):

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

            self.assertCountEqual(response['items'], expected_items)

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

            self.assertCountEqual(response['items'], expected_items)

    @mock.patch('aquascope.webserver.data_access.storage.blob.make_blob_url')
    def test_api_can_get_items_by_empty_species(self, mock_make_blob_url):
        mock_make_blob_url.return_value = 'mockedurl'
        with self.app.app_context():
            request_data = {
                'species': ''
            }
            res = self.client().get('/items', query_string=request_data, headers=self.headers)
            self.assertEqual(res.status_code, 200)

            response = res.json
            expected_items = [DUMMY_ITEMS[1], DUMMY_ITEMS[3]]
            expected_items = [item.serializable() for item in expected_items]

            self.assertCountEqual(response['items'], expected_items)

    @mock.patch('aquascope.webserver.data_access.storage.blob.make_blob_url')
    def test_api_can_get_items_with_bad_argument(self, mock_make_blob_url):
        mock_make_blob_url.return_value = 'mockedurl'
        with self.app.app_context():
            request_data = {
                'invalid_key': [True, '']
            }
            res = self.client().get('/items', query_string=request_data, headers=self.headers)
            self.assertEqual(res.status_code, 400)

    @mock.patch('aquascope.webserver.data_access.storage.blob.make_blob_url')
    def test_api_can_get_items_with_empty_request(self, mock_make_blob_url):
        mock_make_blob_url.return_value = 'mockedurl'
        with self.app.app_context():
            request_data = {}
            res = self.client().get('/items', query_string=request_data, headers=self.headers)
            self.assertEqual(res.status_code, 200)

            response = res.json
            expected_items = DUMMY_ITEMS
            expected_items = [item.serializable() for item in expected_items]

            self.assertCountEqual(response['items'], expected_items)

    @mock.patch('aquascope.webserver.data_access.storage.blob.make_blob_url')
    def test_api_can_get_items_with_time_range(self, mock_make_blob_url):
        mock_make_blob_url.return_value = 'mockedurl'
        with self.app.app_context():
            request_data = {
                'acquisition_time_start': '2019-01-07T18:06:34.151Z',
                'acquisition_time_end': '2019-01-12T18:06:34.151Z'
            }
            res = self.client().get('/items', query_string=request_data, headers=self.headers)
            self.assertEqual(res.status_code, 200)

            response = res.json
            expected_items = [DUMMY_ITEMS[2]]
            expected_items = [item.serializable() for item in expected_items]

            self.assertCountEqual(response['items'], expected_items)

class TestPostItems(FlaskAppTestCase):

    def test_api_can_post_update_pairs(self):
        with self.app.app_context():

            item0 = copy.deepcopy(DUMMY_ITEMS[0])
            item0 = item0.get_dict()
            item0 = Item.from_db_data(list(self.db.items.find(item0))[0])

            replace_item0 = copy.deepcopy(item0)
            replace_item0.dead = True

            item1 = copy.deepcopy(DUMMY_ITEMS[1])
            item1 = item1.get_dict()
            item1 = Item.from_db_data(list(self.db.items.find(item1))[0])

            replace_item1 = copy.deepcopy(item1)
            replace_item1.broken = True

            request_data = json.dumps([
                {
                    'current': item0.serializable(),
                    'update': replace_item0.serializable()
                },
                {
                    'current': item1.serializable(),
                    'update': replace_item1.serializable()
                }
            ])

            res = self.client().post('/items', data=request_data, headers=self.headers)
            self.assertEqual(res.status_code, 200)

            response = res.json
            self.assertEqual(response['matched'], 2)
            self.assertEqual(response['modified'], 2)

    def test_api_can_post_with_bad_argument(self):
        item0 = copy.deepcopy(DUMMY_ITEMS[0])
        item0 = item0.get_dict()
        item0 = Item.from_db_data(list(self.db.items.find(item0))[0])

        replace_item0 = copy.deepcopy(item0)
        replace_item0.dead = True

        request_data = json.dumps([
            {
                'current': item0.serializable(),
                'update': replace_item0.serializable(),
                'dummy': 'value'
            }
        ])

        res = self.client().post('/items', data=request_data, headers=self.headers)
        self.assertEqual(res.status_code, 400)

    def test_api_can_post_with_bad_argument_type(self):
        item0 = copy.deepcopy(DUMMY_ITEMS[0])
        item0 = item0.get_dict()
        item0 = Item.from_db_data(list(self.db.items.find(item0))[0])

        replace_item0 = copy.deepcopy(item0)
        replace_item0.dead = 56

        request_data = json.dumps([
            {
                'current': item0.serializable(),
                'update': replace_item0.serializable()
            }
        ])

        res = self.client().post('/items', data=request_data, headers=self.headers)
        self.assertEqual(res.status_code, 400)


if __name__ == '__main__':
    unittest.main()
