import os
from unittest import mock

import celery

from aquascope.tests.aquascope.webserver.data_access.db.dummy_uploads import (DUMMY_UPLOADS_WITH_DEFAULT_PROJECTION,
                                                                              DUMMY_UPLOADS)
from aquascope.tests.flask_app_test_case import FlaskAppTestCase

TEST_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              '../../../../../data/5p0xMAG_small/features.tsv')


class TestPutUpload(FlaskAppTestCase):

    @mock.patch.object(celery.Celery, 'send_task', return_value=None)
    def test_api_can_put_file(self, mock_celery_send_task):
        with self.app.app_context():
            with open(TEST_FILE_PATH, 'rb') as data:
                res = self.client().put('/upload/dummy_file',
                                        data=data,
                                        headers=self.headers)
                self.assertEqual(res.status_code, 204)


class TestGetUpload(FlaskAppTestCase):

    def test_api_can_get_existing_upload(self):
        with self.app.app_context():
            for upload in DUMMY_UPLOADS:
                res = self.client().get(f'/upload/{str(upload._id)}', headers=self.headers)
                self.assertEqual(res.status_code, 200)

                response = res.json
                self.assertEqual(upload.serializable(), response)

    def test_api_cant_get_nonexisting_upload(self):
        with self.app.app_context():
            res = self.client().get('/upload/dummy_upload_id', headers=self.headers)
            self.assertEqual(res.status_code, 400)

            res = self.client().get('/upload/999000000000000000001003', headers=self.headers)
            self.assertEqual(res.status_code, 400)


class TestGetUploadList(FlaskAppTestCase):
    def test_api_can_get_upload_list(self):
        with self.app.app_context():
            res = self.client().get('/upload/list', headers=self.headers)
            self.assertEqual(res.status_code, 200)

            response = res.json
            expected_uploads = [upload.serializable() for upload in DUMMY_UPLOADS_WITH_DEFAULT_PROJECTION]
            self.assertCountEqual(response, expected_uploads)
