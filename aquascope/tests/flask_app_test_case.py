import os
from passlib.hash import pbkdf2_sha256 as sha256
import unittest
from unittest import mock

from azure.storage.blob.blockblobservice import BlockBlobService
from flask import current_app as app
from flask_jwt_extended import create_access_token
import mongomock

from aquascope.tests.aquascope.webserver.data_access.db.dummy_uploads import DUMMY_UPLOADS
from aquascope.tests.aquascope.webserver.data_access.db.dummy_items import DUMMY_ITEMS
from aquascope.webserver.app import make_app
from aquascope.webserver.data_access.storage import blob
from aquascope.webserver.data_access.util import populate_db_with_items, populate_db_with_uploads

MONGO_CONNECTION_STRING = 'mongodb://example.server.com/aquascopedb'


class FlaskAppTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        if 'MONGO_TEST_DB_CONNECTION_STRING' in os.environ:
            from pymongo import MongoClient
            client = MongoClient(os.environ['MONGO_TEST_DB_CONNECTION_STRING'])
        else:
            client = mongomock.MongoClient(MONGO_CONNECTION_STRING)

        if 'STORAGE_CONNECTION_STRING' in os.environ:
            storage_connection_string = os.environ['STORAGE_CONNECTION_STRING']
        else:
            raise ValueError('STORAGE_CONNECTION_STRING environment variable is required to be set'
                             'to run this test')

        cls.db = client.get_database()

        cls.auth_user = 'testuser'
        cls.auth_pass_raw = 'testpassword'
        auth_pass = sha256.hash(cls.auth_pass_raw)

        cls.app = make_app(cls.db, storage_connection_string, 'jwtdummysecret', cls.auth_user, auth_pass,
                           environment='TESTING', celery_user='',
                           celery_password='', celery_address='')

    def purge_storage(self):
        storage_client = self.app.config['storage_client']
        containers = blob.list_containers(storage_client)
        for container in containers:
            blob.delete_container(storage_client, container)

    def purge_db(self):
        self.db.items.drop()
        self.db.uploads.drop()

    def setUp(self):
        with self.app.app_context():
            self.client = app.test_client
            self.purge_db()
            self.purge_storage()
            populate_db_with_items(DUMMY_ITEMS, self.db)
            populate_db_with_uploads(DUMMY_UPLOADS, self.db)

            access_token = create_access_token('testuser')
            self.headers = {
                'Authorization': 'Bearer {}'.format(access_token)
            }

    def tearDown(self):
        with self.app.app_context():
            self.purge_db()
            self.purge_storage()
