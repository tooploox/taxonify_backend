import os
import tempfile
import urllib.request

import dateutil
import pandas as pd
from bson import ObjectId
from flask import json

from aquascope.tests.aquascope.webserver.data_access.db.dummy_items import DUMMY_ITEMS
from aquascope.tests.flask_app_test_case import FlaskAppTestCase
from aquascope.webserver.data_access.db.items import MORPHOMETRIC_FIELDS, Item


class TestGetPagedItems(FlaskAppTestCase):

    @staticmethod
    def url_to_items(url):
        with tempfile.TemporaryDirectory() as tmpdirname:
            tmp_filepath = os.path.join(tmpdirname, 'data.tsv')
            urllib.request.urlretrieve(url, tmp_filepath)

            converters = {
                'acquisition_time': lambda x: dateutil.parser.parse(x),
                '_id': lambda x: ObjectId(str(x)),
                **{k: lambda x: float(x) for k in MORPHOMETRIC_FIELDS}
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
            self.assertTrue('url' in response)

            items = self.url_to_items(response['url'])
            items = [item.serializable() for item in items]
            expected_items = [item.serializable() for item in DUMMY_ITEMS]
            self.assertCountEqual(items, expected_items)
