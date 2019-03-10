import ast
import os
import tempfile

import dateutil
import pandas as pd
from bson import ObjectId
from flask import json
import requests

from aquascope.tests.aquascope.webserver.data_access.db.dummy_items import DUMMY_ITEMS, DUMMY_ITEMS_WITH_TAGS
from aquascope.tests.flask_app_test_case import FlaskAppTestCase
from aquascope.webserver.data_access.db.items import ANNOTABLE_FIELDS, Item, MORPHOMETRIC_FIELDS


class TestGetPagedItems(FlaskAppTestCase):

    @staticmethod
    def url_to_items(url):
        with tempfile.TemporaryDirectory() as tmpdirname:
            tmp_filepath = os.path.join(tmpdirname, 'data.tsv')
            req = requests.get(url)
            with open(tmp_filepath, 'wb') as f:
                f.write(req.content)

            converters = {
                'acquisition_time': lambda x: dateutil.parser.parse(x),
                '_id': lambda x: ObjectId(str(x)),
                'upload_id': lambda x: ObjectId(str(x)),
                'tags': ast.literal_eval,
                **{k: lambda x: float(x) for k in MORPHOMETRIC_FIELDS},
                **{f'{k}_modification_time': lambda x: dateutil.parser.parse(x) if x else None for k in ANNOTABLE_FIELDS}
            }
            df = pd.read_csv(tmp_filepath, converters=converters, sep='\t')
            df = df.replace({pd.np.nan: None})

            items = [Item(item) for item in df.to_dict('index').values()]
            return items

    def test_api_can_get_export_data_with_negative_limit(self):
        with self.app.app_context():
            request_data = {
                'limit': -1
            }
            res = self.client().get('/export', query_string=request_data, headers=self.headers)
            self.assertEqual(res.status_code, 400)

            wrong_parameters = ['limit']
            res_wrong_parameters = [item['parameter'] for item in json.loads(res.data)["messages"]]
            self.assertCountEqual(wrong_parameters, res_wrong_parameters)

    def test_api_can_get_export_with_all_items(self):
        with self.app.app_context():
            request_data = {}
            res = self.client().get('/export', query_string=request_data, headers=self.headers)
            self.assertEqual(res.status_code, 200)

            response = res.json
            self.assertEqual(response['status'], 'ok')
            self.assertTrue('url' in response)

            items = self.url_to_items(response['url'])
            items = [item.serializable() for item in items]
            expected_items = [item.serializable() for item in DUMMY_ITEMS_WITH_TAGS]
            self.assertCountEqual(items, expected_items)

    def test_api_can_get_export_with_limit_to_single_item(self):
        with self.app.app_context():
            request_data = {
                'limit': 1
            }
            res = self.client().get('/export', query_string=request_data, headers=self.headers)
            self.assertEqual(res.status_code, 200)

            response = res.json
            self.assertEqual(response['status'], 'ok')
            self.assertTrue('url' in response)

            items = self.url_to_items(response['url'])
            items = [item.serializable() for item in items]
            expected_items = [DUMMY_ITEMS_WITH_TAGS[0].serializable()]
            self.assertCountEqual(items, expected_items)

    def test_api_can_get_export_with_attribute_filter(self):
        with self.app.app_context():
            request_data = {
                'eating': True
            }
            res = self.client().get('/export', query_string=request_data, headers=self.headers)
            self.assertEqual(res.status_code, 200)

            response = res.json
            self.assertEqual(response['status'], 'ok')
            self.assertTrue('url' in response)

            items = self.url_to_items(response['url'])
            items = [item.serializable() for item in items]
            expected_items = [item.serializable() for item in DUMMY_ITEMS_WITH_TAGS if item.eating]
            self.assertCountEqual(items, expected_items)

    def test_api_can_get_export_with_taxonomy_filter(self):
        with self.app.app_context():
            request_data = {
                'empire': 'prokaryota'
            }
            res = self.client().get('/export', query_string=request_data, headers=self.headers)
            self.assertEqual(res.status_code, 200)

            response = res.json
            self.assertEqual(response['status'], 'ok')
            self.assertTrue('url' in response)

            items = self.url_to_items(response['url'])
            items = [item.serializable() for item in items]
            expected_items = [item.serializable() for item in DUMMY_ITEMS_WITH_TAGS if item.empire is 'prokaryota']
            self.assertCountEqual(items, expected_items)

    def test_api_can_get_export_with_filters_and_limit(self):
        with self.app.app_context():
            request_data = {
                'eating': True,
                'empire': 'prokaryota',
                'limit': 1
            }
            res = self.client().get('/export', query_string=request_data, headers=self.headers)
            self.assertEqual(res.status_code, 200)

            response = res.json
            self.assertEqual(response['status'], 'ok')
            self.assertTrue('url' in response)

            items = self.url_to_items(response['url'])
            items = [item.serializable() for item in items]
            expected_items = [item.serializable() for item in DUMMY_ITEMS_WITH_TAGS[:1]]
            self.assertCountEqual(items, expected_items)

    def test_api_can_get_export_with_filter_that_doesnt_match_any_items(self):
        with self.app.app_context():
            request_data = {
                'empire': 'eukaryota'
            }
            res = self.client().get('/export', query_string=request_data, headers=self.headers)
            self.assertEqual(res.status_code, 200)

            response = res.json
            self.assertEqual(response['status'], 'empty')
            self.assertFalse('url' in response)
