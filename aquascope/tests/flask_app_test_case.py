import os
from passlib.hash import pbkdf2_sha256 as sha256
import unittest
from unittest import mock

from azure.storage.blob.blockblobservice import BlockBlobService
from flask import current_app as app
from flask_jwt_extended import create_access_token
import mongomock

from aquascope.webserver.app import make_app
from aquascope.webserver.data_access.util import populate_db_with_items
from aquascope.tests.aquascope.webserver.data_access.db.dummy_items import DUMMY_ITEMS

MONGO_CONNECTION_STRING = 'mongodb://example.server.com/aquascopedb'


class FlaskAppTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        if 'MONGO_TEST_DB_CONNECTION_STRING' in os.environ:
            from pymongo import MongoClient
            client = MongoClient(os.environ['MONGO_TEST_DB_CONNECTION_STRING'])
        else:
            client = mongomock.MongoClient(MONGO_CONNECTION_STRING)
        cls.db = client.get_database()

        cls.auth_user = 'testuser'
        cls.auth_pass_raw = 'testpassword'
        auth_pass = sha256.hash(cls.auth_pass_raw)

        with mock.patch.object(BlockBlobService, '__init__', lambda x, connection_string: None):
            cls.app = make_app(cls.db, '', 'jwtdummysecret', cls.auth_user, auth_pass,
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
