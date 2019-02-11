import os
from unittest import mock

import celery

from aquascope.tests.flask_app_test_case import FlaskAppTestCase

TEST_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              '../../../../../data/metadata.csv')


class TestPutUpload(FlaskAppTestCase):

    @mock.patch.object(celery.Celery, 'send_task', return_value=None)
    def test_api_can_put_file(self, send_task_mock):
        with self.app.app_context():
            with open(TEST_FILE_PATH, 'rb') as data:
                res = self.client().put('/upload/dummy_file',
                                        data=data,
                                        headers=self.headers)
                self.assertEqual(res.status_code, 200)
