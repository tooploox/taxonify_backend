import unittest
from unittest import mock

from aquascope.tests.flask_app_test_case import FlaskAppTestCase
from aquascope.webserver.data_access.conversions import GROUP_ID_TO_CONTAINER


class TestGetSas(FlaskAppTestCase):

    @mock.patch('aquascope.webserver.data_access.storage.blob.generate_container_download_sas')
    def test_api_can_get_sas_token_for_valid_destination(self, mock_sas):
        mocked_sas = 'mockedsas'
        mock_sas.return_value = mocked_sas
        valid_destinations = tuple(GROUP_ID_TO_CONTAINER.keys())

        with self.app.app_context():
            request_data = {
                'destination': valid_destinations[0]
            }
            res = self.client().get('/sas', query_string=request_data, headers=self.headers)
            self.assertEqual(res.status_code, 200)

            response = res.json
            self.assertEqual(response['token'], mocked_sas)

    @mock.patch('aquascope.webserver.data_access.storage.blob.generate_container_download_sas')
    def test_api_can_get_sas_token_for_invalid_destination(self, mock_sas):
        mocked_sas = 'mockedsas'
        mock_sas.return_value = mocked_sas
        valid_destinations = tuple(GROUP_ID_TO_CONTAINER.keys())

        with self.app.app_context():
            request_data = {
                'destination': valid_destinations[0] + 'dummy'
            }
            res = self.client().get('/sas', query_string=request_data, headers=self.headers)
            self.assertEqual(res.status_code, 400)

    @mock.patch('aquascope.webserver.data_access.storage.blob.generate_container_download_sas')
    def test_api_can_get_sas_token_for_missing_destination_argument(self, mock_sas):
        mocked_sas = 'mockedsas'
        mock_sas.return_value = mocked_sas

        with self.app.app_context():
            request_data = {}
            res = self.client().get('/sas', query_string=request_data, headers=self.headers)
            self.assertEqual(res.status_code, 400)


if __name__ == '__main__':
    unittest.main()
