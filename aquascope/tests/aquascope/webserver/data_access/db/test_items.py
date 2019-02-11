import copy
import unittest

import dateutil
from bson import ObjectId

from aquascope.tests.aquascope.webserver.data_access.db.dummy_items import DUMMY_ITEMS
from aquascope.tests.flask_app_test_case import FlaskAppTestCase
from aquascope.webserver.data_access.db.items import find_items, bulk_replace


class TestFindItems(FlaskAppTestCase):

    def test_bool_nullable_field_with_bool(self):
        with self.app.app_context():
            find_query = {
                'eating': [True]
            }

            db = self.app.config['db']
            res = list(find_items(db, **find_query))
            res = [res['_id'] for res in res]
            expected = [
                ObjectId('000000000000000000000000'),
                ObjectId('000000000000000000000001')
            ]
            self.assertCountEqual(res, expected)

    def test_bool_nullable_field_with_none(self):
        with self.app.app_context():
            find_query = {
                'eating': [None]
            }

            db = self.app.config['db']
            res = list(find_items(db, **find_query))
            res = [res['_id'] for res in res]
            expected = [
                ObjectId('000000000000000000000003'),
                ObjectId('000000000000000000000004')
            ]
            self.assertCountEqual(res, expected)

    def test_bool_nullable_field_with_bool_and_none(self):
        with self.app.app_context():
            find_query = {
                'eating': [True, None]
            }

            db = self.app.config['db']
            res = list(find_items(db, **find_query))
            res = [res['_id'] for res in res]
            expected = [
                ObjectId('000000000000000000000000'),
                ObjectId('000000000000000000000001'),
                ObjectId('000000000000000000000003'),
                ObjectId('000000000000000000000004')
            ]
            self.assertCountEqual(res, expected)

    def test_datetime_field(self):
        with self.app.app_context():
            find_query = {
                'acquisition_time_start': dateutil.parser.parse('2019-01-11T18:06:34.151Z')
            }

            db = self.app.config['db']
            res = list(find_items(db, **find_query))
            res = [res['_id'] for res in res]
            expected = [
                ObjectId('000000000000000000000000'),
                ObjectId('000000000000000000000001')
            ]
            self.assertCountEqual(res, expected)

    def test_datetime_fields_range(self):
        with self.app.app_context():
            find_query = {
                'acquisition_time_start': dateutil.parser.parse('2019-01-02T18:06:34.151Z'),
                'acquisition_time_end': dateutil.parser.parse('2019-01-11T18:06:34.151Z')
            }

            db = self.app.config['db']
            res = list(find_items(db, **find_query))
            res = [res['_id'] for res in res]
            expected = [
                ObjectId('000000000000000000000003'),
                ObjectId('000000000000000000000002')
            ]
            self.assertCountEqual(res, expected)

    def test_fields_combination(self):
        with self.app.app_context():
            find_query = {
                'species': 'sp',
                'dead': [True, False],
                'acquisition_time_end': dateutil.parser.parse('2019-01-15T18:06:34.151Z')
            }

            db = self.app.config['db']
            res = list(find_items(db, **find_query))
            res = [res['_id'] for res in res]
            expected = [
                ObjectId('000000000000000000000002')
            ]
            self.assertCountEqual(res, expected)


class TestBulkReplace(FlaskAppTestCase):

    def test_bulk_replace_outdated_object(self):
        with self.app.app_context():
            item = copy.deepcopy(DUMMY_ITEMS[0])
            item.dead = True
            replace_item = copy.deepcopy(item)

            update_pairs = [
                (item, replace_item)
            ]

            db = self.app.config['db']
            result = bulk_replace(db, update_pairs)

            self.assertEqual(result.matched_count, 0)
            self.assertEqual(result.modified_count, 0)

    def test_bulk_replace_no_changes(self):
        with self.app.app_context():
            item = DUMMY_ITEMS[0]
            replace_item = copy.deepcopy(item)

            update_pairs = [
                (item, replace_item)
            ]

            db = self.app.config['db']
            result = bulk_replace(db, update_pairs)

            self.assertEqual(result.matched_count, 1)
            self.assertEqual(result.modified_count, 0)

    def test_bulk_replace_single_object(self):
        with self.app.app_context():
            item = DUMMY_ITEMS[0]
            replace_item = copy.deepcopy(item)
            replace_item.dead = True

            update_pairs = [
                (item, replace_item)
            ]

            db = self.app.config['db']
            result = bulk_replace(db, update_pairs)

            self.assertEqual(result.matched_count, 1)
            self.assertEqual(result.modified_count, 1)

    def test_bulk_replace_single_object_twice(self):
        with self.app.app_context():
            item = DUMMY_ITEMS[0]
            replace_item0 = copy.deepcopy(item)
            replace_item0.dead = True

            replace_item1 = copy.deepcopy(item)
            replace_item1.colony = True

            update_pairs = [
                (item, replace_item0),
                (item, replace_item1)

            ]

            db = self.app.config['db']
            result = bulk_replace(db, update_pairs)

            db_item = self.db.items.find_one({'_id': item._id})
            self.assertDictEqual(replace_item0.get_dict(), db_item)

            self.assertEqual(result.matched_count, 1)
            self.assertEqual(result.modified_count, 1)

    def test_bulk_replace_multiple_objects(self):
        with self.app.app_context():
            item0 = DUMMY_ITEMS[0]
            replace_item0 = copy.deepcopy(item0)
            replace_item0.dead = True

            item1 = DUMMY_ITEMS[1]
            replace_item1 = copy.deepcopy(item1)
            replace_item1.male = True

            update_pairs = [
                (item0, replace_item0),
                (item1, replace_item1)
            ]

            db = self.app.config['db']
            result = bulk_replace(db, update_pairs)

            self.assertEqual(result.matched_count, 2)
            self.assertEqual(result.modified_count, 2)

    def test_bulk_replace_multiple_objects_with_partial_modify(self):
        with self.app.app_context():
            item0 = DUMMY_ITEMS[0]
            replace_item0 = copy.deepcopy(item0)
            replace_item0.dead = True

            item1 = DUMMY_ITEMS[1]
            replace_item1 = copy.deepcopy(item1)

            update_pairs = [
                (item0, replace_item0),
                (item1, replace_item1)
            ]

            db = self.app.config['db']
            result = bulk_replace(db, update_pairs)

            self.assertEqual(result.matched_count, 2)
            self.assertEqual(result.modified_count, 1)

    def test_bulk_replace_multiple_objects_with_partial_match(self):
        with self.app.app_context():
            item0 = DUMMY_ITEMS[0]
            item0.broken = True
            replace_item0 = copy.deepcopy(item0)
            replace_item0.dead = True

            item1 = DUMMY_ITEMS[1]
            replace_item1 = copy.deepcopy(item1)
            replace_item1.male = True

            update_pairs = [
                (item0, replace_item0),
                (item1, replace_item1)
            ]

            db = self.app.config['db']
            result = bulk_replace(db, update_pairs)

            self.assertEqual(result.matched_count, 1)
            self.assertEqual(result.modified_count, 1)


if __name__ == '__main__':
    unittest.main()
