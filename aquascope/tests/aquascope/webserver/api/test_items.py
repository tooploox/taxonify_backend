import copy
import math
import unittest
from unittest import mock

from flask import json

from aquascope.tests.aquascope.webserver.data_access.db.dummy_items import DUMMY_ITEMS, \
    DUMMY_ITEMS_WITH_DEFAULT_PROJECTION
from aquascope.tests.flask_app_test_case import FlaskAppTestCase
from aquascope.webserver.data_access.db import Item

MONGO_CONNECTION_STRING = 'mongodb://example.server.com/aquascopedb'


class TestGetPagedItems(FlaskAppTestCase):

    @mock.patch('aquascope.webserver.data_access.storage.blob.make_blob_url')
    def test_api_can_get_single_page(self, mock_make_blob_url):
        mock_make_blob_url.return_value = 'mockedurl'
        with self.app.app_context():
            self.app.config['page_size'] = 2

            request_data = {}
            res = self.client().get('/items/paged', query_string=request_data, headers=self.headers)
            self.assertEqual(res.status_code, 200)

            response = res.json
            expected_items = [DUMMY_ITEMS_WITH_DEFAULT_PROJECTION[0], DUMMY_ITEMS_WITH_DEFAULT_PROJECTION[1]]
            expected_items = [item.serializable() for item in expected_items]

            self.assertCountEqual(response['items'], expected_items)
            self.assertTrue('continuation_token' in response)
            self.assertEqual(2, response['continuation_token'])

    @mock.patch('aquascope.webserver.data_access.storage.blob.make_blob_url')
    def test_api_can_get_all_items_in_one_page(self, mock_make_blob_url):
        mock_make_blob_url.return_value = 'mockedurl'
        with self.app.app_context():
            self.app.config['page_size'] = 500

            request_data = {}
            res = self.client().get('/items/paged', query_string=request_data, headers=self.headers)
            self.assertEqual(res.status_code, 200)

            response = res.json
            expected_items = DUMMY_ITEMS_WITH_DEFAULT_PROJECTION
            expected_items = [item.serializable() for item in expected_items]

            self.assertCountEqual(response['items'], expected_items)
            self.assertFalse('continuation_token' in response)

    @mock.patch('aquascope.webserver.data_access.storage.blob.make_blob_url')
    def test_api_can_get_requested_page(self, mock_make_blob_url):
        mock_make_blob_url.return_value = 'mockedurl'
        with self.app.app_context():
            self.app.config['page_size'] = 2

            request_data = {
                'continuation_token': 2
            }
            res = self.client().get('/items/paged', query_string=request_data, headers=self.headers)
            self.assertEqual(res.status_code, 200)

            response = res.json
            expected_items = [DUMMY_ITEMS_WITH_DEFAULT_PROJECTION[2], DUMMY_ITEMS_WITH_DEFAULT_PROJECTION[3]]
            expected_items = [item.serializable() for item in expected_items]

            self.assertCountEqual(response['items'], expected_items)
            self.assertTrue('continuation_token' in response)
            self.assertEqual(3, response['continuation_token'])

    @mock.patch('aquascope.webserver.data_access.storage.blob.make_blob_url')
    def test_api_can_get_last_page(self, mock_make_blob_url):
        mock_make_blob_url.return_value = 'mockedurl'
        with self.app.app_context():
            self.app.config['page_size'] = 2

            last_page_idx = math.ceil(len(DUMMY_ITEMS_WITH_DEFAULT_PROJECTION) / self.app.config['page_size'])
            request_data = {
                'continuation_token': last_page_idx
            }
            res = self.client().get('/items/paged', query_string=request_data, headers=self.headers)
            self.assertEqual(res.status_code, 200)

            response = res.json

            expected_items_start = (last_page_idx - 1) * self.app.config['page_size']
            expected_items = DUMMY_ITEMS_WITH_DEFAULT_PROJECTION[
                             expected_items_start:]
            expected_items = [item.serializable() for item in expected_items]

            self.assertCountEqual(response['items'], expected_items)
            self.assertFalse('continuation_token' in response)

    @mock.patch('aquascope.webserver.data_access.storage.blob.make_blob_url')
    def test_api_cant_get_negative_page(self, mock_make_blob_url):
        mock_make_blob_url.return_value = 'mockedurl'
        with self.app.app_context():
            self.app.config['page_size'] = 2

            request_data = {
                'continuation_token': -10
            }
            res = self.client().get('/items/paged', query_string=request_data, headers=self.headers)
            self.assertEqual(res.status_code, 400)

            wrong_parameters = ['continuation_token']
            res_wrong_parameters = [item['parameter'] for item in json.loads(res.data)["messages"]]
            self.assertCountEqual(wrong_parameters, res_wrong_parameters)

    @mock.patch('aquascope.webserver.data_access.storage.blob.make_blob_url')
    def test_api_cant_get_zero_page(self, mock_make_blob_url):
        mock_make_blob_url.return_value = 'mockedurl'
        with self.app.app_context():
            self.app.config['page_size'] = 2

            request_data = {
                'continuation_token': 0
            }
            res = self.client().get('/items/paged', query_string=request_data, headers=self.headers)
            self.assertEqual(res.status_code, 400)

            wrong_parameters = ['continuation_token']
            res_wrong_parameters = [item['parameter'] for item in json.loads(res.data)["messages"]]
            self.assertCountEqual(wrong_parameters, res_wrong_parameters)

    @mock.patch('aquascope.webserver.data_access.storage.blob.make_blob_url')
    def test_api_can_get_zero_items_because_page_is_too_far(self, mock_make_blob_url):
        mock_make_blob_url.return_value = 'mockedurl'
        with self.app.app_context():
            self.app.config['page_size'] = 2

            request_data = {
                'continuation_token': 10
            }
            res = self.client().get('/items/paged', query_string=request_data, headers=self.headers)
            self.assertEqual(res.status_code, 200)

            response = res.json
            expected_items = []
            self.assertCountEqual(response['items'], expected_items)
            self.assertFalse('continuation_token' in response)


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
            expected_items = [DUMMY_ITEMS_WITH_DEFAULT_PROJECTION[0], DUMMY_ITEMS_WITH_DEFAULT_PROJECTION[1]]
            expected_items = [item.serializable() for item in expected_items]

            self.assertCountEqual(response['items'], expected_items)

    @mock.patch('aquascope.webserver.data_access.storage.blob.make_blob_url')
    def test_api_can_get_items_by_taxonomy(self, mock_make_blob_url):
        mock_make_blob_url.return_value = 'mockedurl'
        with self.app.app_context():
            request_data = {
                'empire': 'prokaryota'
            }
            res = self.client().get('/items', query_string=request_data, headers=self.headers)
            self.assertEqual(res.status_code, 200)

            response = res.json
            expected_items = [item.serializable() for item in DUMMY_ITEMS_WITH_DEFAULT_PROJECTION[:4]]

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
            expected_items = [DUMMY_ITEMS_WITH_DEFAULT_PROJECTION[0], DUMMY_ITEMS_WITH_DEFAULT_PROJECTION[1],
                              DUMMY_ITEMS_WITH_DEFAULT_PROJECTION[3], DUMMY_ITEMS_WITH_DEFAULT_PROJECTION[4]]
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
            expected_items = [DUMMY_ITEMS_WITH_DEFAULT_PROJECTION[1], DUMMY_ITEMS_WITH_DEFAULT_PROJECTION[3]]
            expected_items = [item.serializable() for item in expected_items]

            self.assertCountEqual(response['items'], expected_items)

    def test_api_cant_get_items_with_bad_argument(self):
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
            expected_items = DUMMY_ITEMS_WITH_DEFAULT_PROJECTION
            expected_items = [item.serializable() for item in expected_items]

            self.assertCountEqual(response['items'], expected_items)

    @mock.patch('aquascope.webserver.data_access.storage.blob.make_blob_url')
    def test_api_can_get_items_with_acquisition_time_range(self, mock_make_blob_url):
        mock_make_blob_url.return_value = 'mockedurl'
        with self.app.app_context():
            request_data = {
                'acquisition_time_start': '2019-01-07T18:06:34.151Z',
                'acquisition_time_end': '2019-01-12T18:06:34.151Z'
            }
            res = self.client().get('/items', query_string=request_data, headers=self.headers)
            self.assertEqual(res.status_code, 200)

            response = res.json
            expected_items = [DUMMY_ITEMS_WITH_DEFAULT_PROJECTION[2]]
            expected_items = [item.serializable() for item in expected_items]

            self.assertCountEqual(response['items'], expected_items)

    def test_api_get_emits_errors_for_all_wrong_parameters(self):
        with self.app.app_context():
            res = self.client().get('/items', query_string="eating=bar&multiple_species=foobar&eating=foo",
                                    headers=self.headers)
            wrong_parameters = ['eating.0', 'eating.1', 'multiple_species.0']

            res_wrong_parameters = [item['parameter'] for item in json.loads(res.data)["messages"]]
            self.assertCountEqual(wrong_parameters, res_wrong_parameters)

    @mock.patch('aquascope.webserver.data_access.storage.blob.make_blob_url')
    def test_api_can_get_items_with_given_field_last_modified_by_given_user(self, mock_make_blob_url):
        mock_make_blob_url.return_value = 'mockedurl'
        with self.app.app_context():
            request_data = {
                'eating': [True, ''],
                'modified_by': 'user1'
            }
            res = self.client().get('/items', query_string=request_data, headers=self.headers)
            self.assertEqual(res.status_code, 200)

            response = res.json
            expected_items = [DUMMY_ITEMS_WITH_DEFAULT_PROJECTION[0], DUMMY_ITEMS_WITH_DEFAULT_PROJECTION[3]]
            expected_items = [item.serializable() for item in expected_items]

            self.assertCountEqual(response['items'], expected_items)

    @mock.patch('aquascope.webserver.data_access.storage.blob.make_blob_url')
    def test_api_can_get_items_with_given_fields_last_modified_by_given_user(self, mock_make_blob_url):
        mock_make_blob_url.return_value = 'mockedurl'
        with self.app.app_context():
            request_data = {
                'eating': [True, ''],
                'empire': 'prokaryota',
                'modified_by': 'user1'
            }
            res = self.client().get('/items', query_string=request_data, headers=self.headers)
            self.assertEqual(res.status_code, 200)

            response = res.json
            expected_items = [DUMMY_ITEMS_WITH_DEFAULT_PROJECTION[0], DUMMY_ITEMS_WITH_DEFAULT_PROJECTION[3]]
            expected_items = [item.serializable() for item in expected_items]

            self.assertCountEqual(response['items'], expected_items)

    @mock.patch('aquascope.webserver.data_access.storage.blob.make_blob_url')
    def test_api_can_get_items_with_given_fields_last_modified_by_given_user_that_have_single_match(self,
                                                                                                mock_make_blob_url):
        mock_make_blob_url.return_value = 'mockedurl'
        with self.app.app_context():
            request_data = {
                'eating': True,
                'empire': 'prokaryota',
                'modified_by': 'user1'
            }
            res = self.client().get('/items', query_string=request_data, headers=self.headers)
            self.assertEqual(res.status_code, 200)

            response = res.json
            expected_items = [DUMMY_ITEMS_WITH_DEFAULT_PROJECTION[0]]
            expected_items = [item.serializable() for item in expected_items]

            self.assertCountEqual(response['items'], expected_items)

    @mock.patch('aquascope.webserver.data_access.storage.blob.make_blob_url')
    def test_api_can_get_zero_items_with_given_fields_last_modified_by_given_user_that_have_no_match(self, mock_make_blob_url):
        mock_make_blob_url.return_value = 'mockedurl'
        with self.app.app_context():
            request_data = {
                'allman': False,
                'eating': [True, ''],
                'empire': 'prokaryota',
                'modified_by': 'user1'
            }
            res = self.client().get('/items', query_string=request_data, headers=self.headers)
            self.assertEqual(res.status_code, 200)

            response = res.json
            expected_items = []
            self.assertCountEqual(response['items'], expected_items)

    @mock.patch('aquascope.webserver.data_access.storage.blob.make_blob_url')
    def test_api_can_get_items_with_any_field_last_modified_by_given_user(self, mock_make_blob_url):
        mock_make_blob_url.return_value = 'mockedurl'
        request_data = {
            'modified_by': 'user2'
        }

        res = self.client().get('/items', query_string=request_data, headers=self.headers)
        self.assertEqual(res.status_code, 200)

        response = res.json
        expected_items = [DUMMY_ITEMS_WITH_DEFAULT_PROJECTION[1], DUMMY_ITEMS_WITH_DEFAULT_PROJECTION[3]]
        expected_items = [item.serializable() for item in expected_items]
        self.assertCountEqual(response['items'], expected_items)

    @mock.patch('aquascope.webserver.data_access.storage.blob.make_blob_url')
    def test_api_can_get_items_with_any_field_last_modified_by_given_user_and_other_nonannotable_criteria(self,
                                                                                                      mock_make_blob_url):
        mock_make_blob_url.return_value = 'mockedurl'
        request_data = {
            'acquisition_time_start': '2019-01-20T02:00:00.001Z',
            'acquisition_time_end': '2019-01-20T12:06:34.151Z',
            'modified_by': 'user2'
        }

        res = self.client().get('/items', query_string=request_data, headers=self.headers)
        self.assertEqual(res.status_code, 200)

        response = res.json
        expected_items = [DUMMY_ITEMS_WITH_DEFAULT_PROJECTION[1]]
        expected_items = [item.serializable() for item in expected_items]
        self.assertCountEqual(response['items'], expected_items)

    @mock.patch('aquascope.webserver.data_access.storage.blob.make_blob_url')
    def test_api_get_zero_items_with_given_fields_last_modified_by_nonexisting_user(self, mock_make_blob_url):
        mock_make_blob_url.return_value = 'mockedurl'
        with self.app.app_context():
            request_data = {
                'eating': [True, ''],
                'empire': 'prokaryota',
                'modified_by': 'nosuchuser1'
            }
            res = self.client().get('/items', query_string=request_data, headers=self.headers)
            self.assertEqual(res.status_code, 200)

            response = res.json
            expected_items = []

            self.assertCountEqual(response['items'], expected_items)

    @mock.patch('aquascope.webserver.data_access.storage.blob.make_blob_url')
    def test_api_get_zero_items_with_any_field_last_modified_by_nonexisting_user(self, mock_make_blob_url):
        mock_make_blob_url.return_value = 'mockedurl'
        with self.app.app_context():
            request_data = {
                'modified_by': 'nosuchuser1'
            }
            res = self.client().get('/items', query_string=request_data, headers=self.headers)
            self.assertEqual(res.status_code, 200)

            response = res.json
            expected_items = []

            self.assertCountEqual(response['items'], expected_items)

    @mock.patch('aquascope.webserver.data_access.storage.blob.make_blob_url')
    def test_api_get_items_with_any_field_last_modified_by_null_user(self, mock_make_blob_url):
        mock_make_blob_url.return_value = 'mockedurl'
        with self.app.app_context():
            request_data = {
                'modified_by': ''
            }
            res = self.client().get('/items', query_string=request_data, headers=self.headers)
            self.assertEqual(res.status_code, 200)

            response = res.json
            expected_items = [DUMMY_ITEMS_WITH_DEFAULT_PROJECTION[2], DUMMY_ITEMS_WITH_DEFAULT_PROJECTION[4]]
            expected_items = [item.serializable() for item in expected_items]

            self.assertCountEqual(response['items'], expected_items)

    @mock.patch('aquascope.webserver.data_access.storage.blob.make_blob_url')
    def test_api_can_get_items_with_given_field_and_modification_time_range(self, mock_make_blob_url):
        mock_make_blob_url.return_value = 'mockedurl'
        with self.app.app_context():
            request_data = {
                'eating': [True, ''],
                'modification_time_start': '2019-01-18T18:00:00.000Z',
                'modification_time_end': '2019-01-25T18:00:00.000Z'
            }
            res = self.client().get('/items', query_string=request_data, headers=self.headers)
            self.assertEqual(res.status_code, 200)

            response = res.json
            expected_items = [DUMMY_ITEMS_WITH_DEFAULT_PROJECTION[0], DUMMY_ITEMS_WITH_DEFAULT_PROJECTION[1]]
            expected_items = [item.serializable() for item in expected_items]

            self.assertCountEqual(response['items'], expected_items)

    @mock.patch('aquascope.webserver.data_access.storage.blob.make_blob_url')
    def test_api_can_get_items_with_given_user_and_modification_time_range(self, mock_make_blob_url):
        mock_make_blob_url.return_value = 'mockedurl'
        with self.app.app_context():
            request_data = {
                'modified_by': 'user1',
                'modification_time_start': '2019-01-18T18:00:00.000Z',
                'modification_time_end': '2019-01-25T18:00:00.000Z'
            }
            res = self.client().get('/items', query_string=request_data, headers=self.headers)
            self.assertEqual(res.status_code, 200)

            response = res.json
            expected_items = [DUMMY_ITEMS_WITH_DEFAULT_PROJECTION[0]]
            expected_items = [item.serializable() for item in expected_items]

            self.assertCountEqual(response['items'], expected_items)


class TestPostItems(FlaskAppTestCase):

    def test_api_can_post_update_pairs(self):
        with self.app.app_context():
            item0 = copy.deepcopy(DUMMY_ITEMS_WITH_DEFAULT_PROJECTION[0])

            replace_item0 = copy.deepcopy(item0)
            replace_item0.dead = True

            item1 = copy.deepcopy(DUMMY_ITEMS_WITH_DEFAULT_PROJECTION[1])

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
        item0 = copy.deepcopy(DUMMY_ITEMS_WITH_DEFAULT_PROJECTION[0])

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
        item0 = copy.deepcopy(DUMMY_ITEMS_WITH_DEFAULT_PROJECTION[0])

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

    def test_api_cant_post_with_empty_list(self):
        request_data = json.dumps([])

        res = self.client().post('/items', data=request_data, headers=self.headers)
        self.assertEqual(res.status_code, 400)

    def test_api_cant_post_with_empty_dict(self):
        request_data = json.dumps({})

        res = self.client().post('/items', data=request_data, headers=self.headers)
        self.assertEqual(res.status_code, 400)

    def test_api_post_emits_errors_for_all_wrong_parameters(self):
        with self.app.app_context():
            item0 = copy.deepcopy(DUMMY_ITEMS_WITH_DEFAULT_PROJECTION[0])

            replace_item0 = copy.deepcopy(item0)
            replace_item0.dead = 56

            replace_item1 = copy.deepcopy(item0)
            replace_item1.foo = "bar"

            request_data = json.dumps([
                {
                    'current': item0.serializable(),
                    'update': replace_item0.serializable()
                },
                {
                    'current': item0.serializable(),
                    'update': replace_item1.serializable()
                },
            ])

            res = self.client().post('/items', data=request_data, headers=self.headers)
            expected_errors = [{'parameter': '0.update.dead', 'errors': ['Not a valid boolean.']},
                               {'parameter': '1.update.foo', 'errors': ['Unknown field.']}]
            response_data = json.loads(res.data)["messages"]
            self.assertCountEqual(expected_errors, response_data)


if __name__ == '__main__':
    unittest.main()
