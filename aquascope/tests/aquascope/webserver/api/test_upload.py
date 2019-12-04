import copy
import os
from unittest import mock

import celery
from bson import ObjectId
from flask import json

from aquascope.tests.aquascope.webserver.data_access.db.dummy_uploads import (DUMMY_UPLOADS_WITH_DEFAULT_PROJECTION,
                                                                              DUMMY_UPLOADS)
from aquascope.tests.flask_app_test_case import FlaskAppTestCase
from aquascope.webserver.data_access.db import upload

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
                self.assertEqual(res.status_code, 200)
                response = res.json
                self.assertTrue(ObjectId.is_valid(response['_id']))


class TestPostUploadTags(FlaskAppTestCase):

    def test_api_can_post_valid_tags_list(self):
        with self.app.app_context():
            upload_doc = copy.deepcopy(DUMMY_UPLOADS[3])
            tags = ['tag1', 'tag2']
            request_data = json.dumps({
                'tags': tags
            })
            res = self.client().post(f'/upload/{str(upload_doc._id)}/tags',
                                     data=request_data, headers=self.headers)
            self.assertEqual(res.status_code, 204)

            db = self.app.config['db']
            upload_after = upload.get(db, upload_doc._id, with_default_projection=False)
            self.assertCountEqual(upload_after.tags, tags)

    def test_api_can_post_empty_tags_list(self):
        with self.app.app_context():
            upload_doc = copy.deepcopy(DUMMY_UPLOADS[3])
            tags = []
            request_data = json.dumps({
                'tags': tags
            })
            res = self.client().post(f'/upload/{str(upload_doc._id)}/tags',
                                     data=request_data, headers=self.headers)
            self.assertEqual(res.status_code, 204)

            db = self.app.config['db']
            upload_after = upload.get(db, upload_doc._id, with_default_projection=False)
            self.assertCountEqual(upload_after.tags, tags)

    def test_api_cant_post_invalid_tags_list(self):
        with self.app.app_context():
            upload_doc = copy.deepcopy(DUMMY_UPLOADS[3])
            invalid_tags = [
                [4],
                ['valid', 4],
                'invalid',
                [False]
            ]

            for tags_list in invalid_tags:
                request_data = json.dumps({
                    'tags': tags_list
                })
                res = self.client().post(f'/upload/{str(upload_doc._id)}/tags',
                                         data=request_data, headers=self.headers)
                self.assertEqual(res.status_code, 400)

                db = self.app.config['db']
                upload_after = upload.get(db, upload_doc._id, with_default_projection=False)
                self.assertCountEqual(upload_after.tags, upload_doc.tags)

    def test_api_cant_post_tags_for_invalid_upload(self):
        with self.app.app_context():
            tags = ['tag1', 'tag2']
            request_data = json.dumps({
                'tags': tags
            })
            res = self.client().post(f'/upload/dummy_upload_id/tags',
                                     data=request_data, headers=self.headers)
            self.assertEqual(res.status_code, 400)

            res = self.client().post(f'/upload/999000000000000000001003/tags',
                                     data=request_data, headers=self.headers)
            self.assertEqual(res.status_code, 400)

    def test_api_cant_post_tags_for_not_finished_upload(self):
        with self.app.app_context():
            tags = ['tag1', 'tag2']
            request_data = json.dumps({
                'tags': tags
            })

            upload_ids = [
                DUMMY_UPLOADS[0]._id, DUMMY_UPLOADS[1]._id, DUMMY_UPLOADS[2]._id,
                DUMMY_UPLOADS[4]._id
            ]

            for upload_id in upload_ids:
                res = self.client().post(f'/upload/{str(upload_id)}/tags',
                                         data=request_data, headers=self.headers)
                self.assertEqual(res.status_code, 400)

    @mock.patch('aquascope.webserver.data_access.storage.blob.make_blob_url')
    def test_api_tags_update_to_non_finished_upload_does_not_propagate_to_items(self, mock_make_blob_url):
        mock_make_blob_url.return_value = 'mockedurl'

        old_tag = DUMMY_UPLOADS[1].tags[1]

        request_data = {
            'tags': [old_tag]
        }
        res = self.client().get('/items', query_string=request_data, headers=self.headers)
        self.assertEqual(res.status_code, 200)
        original_items = res.json['items']
        self.assertTrue(len(original_items) != 0)

        new_tags = ['new_tag1', 'new_tag2']
        request_data = json.dumps({
            'tags': new_tags
        })
        res = self.client().post(f'/upload/{str(DUMMY_UPLOADS[1]._id)}/tags',
                                 data=request_data, headers=self.headers)
        self.assertEqual(res.status_code, 400)

        request_data = {
            'tags': new_tags
        }
        res = self.client().get('/items', query_string=request_data, headers=self.headers)
        self.assertEqual(res.status_code, 200)
        new_items = res.json['items']

        for item in original_items + new_items:
            item.pop('tags')

        self.assertTrue(len(new_items) == 0)

    @mock.patch('aquascope.webserver.data_access.storage.blob.make_blob_url')
    def test_api_tags_update_is_propagated_to_items(self, mock_make_blob_url):
        mock_make_blob_url.return_value = 'mockedurl'

        old_tag = DUMMY_UPLOADS[3].tags[0]

        request_data = {
            'tags': [old_tag]
        }
        res = self.client().get('/items', query_string=request_data, headers=self.headers)
        self.assertEqual(res.status_code, 200)
        original_items = res.json['items']

        new_tags = ['new_tag1', 'new_tag2']
        request_data = json.dumps({
            'tags': new_tags
        })
        res = self.client().post(f'/upload/{str(DUMMY_UPLOADS[3]._id)}/tags',
                                 data=request_data, headers=self.headers)
        self.assertEqual(res.status_code, 204)

        request_data = {
            'tags': new_tags
        }
        res = self.client().get('/items', query_string=request_data, headers=self.headers)
        self.assertEqual(res.status_code, 200)
        new_items = res.json['items']

        for item in original_items + new_items:
            item.pop('tags')

        self.assertCountEqual(original_items, new_items)


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
