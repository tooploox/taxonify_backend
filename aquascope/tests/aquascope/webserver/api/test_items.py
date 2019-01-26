from unittest import mock

from aquascope.tests.aquascope.webserver.data_access.db.dummy_items import DUMMY_ITEMS
from aquascope.tests.flask_app_test_case import FlaskAppTestCase

MONGO_CONNECTION_STRING = 'mongodb://example.server.com/aquascopedb'


class TestItems(FlaskAppTestCase):

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

    @mock.patch('aquascope.webserver.data_access.storage.blob.make_blob_url')
    def test_api_can_get_items_with_bad_argument(self, mock_make_blob_url):
        mock_make_blob_url.return_value = 'mockedurl'
        with self.app.app_context():
            request_data = {
                'eeating': [True, '']
            }
            res = self.client().get('/items', query_string=request_data, headers=self.headers)
            self.assertEqual(res.status_code, 400)
