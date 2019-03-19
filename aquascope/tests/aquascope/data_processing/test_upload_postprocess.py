import os
import tarfile
import tempfile
import unittest

from aquascope.data_processing.upload_postprocess import parse_upload_package
from aquascope.tests.flask_app_test_case import FlaskAppTestCase
from aquascope.webserver.data_access.db import upload
from aquascope.webserver.data_access.util import upload_package_from_stream

DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         '../../../../data/')


class TestParseUploadPackage(FlaskAppTestCase):

    @staticmethod
    def create_package_from_directory(directory_path, output_path, compression='bz2', arcname=None):
        if arcname is None:
            arcname = os.path.basename(directory_path)

        with tarfile.open(output_path, f'w:{compression}') as tar:
            tar.add(directory_path, arcname=arcname)

    def upload_package(self, package_path):
        storage_client = self.app.config['storage_client']
        with open(package_path, 'rb') as filestream:
            upload_id = upload_package_from_stream(os.path.basename(package_path),
                                                   filestream, self.db, storage_client)
            return upload_id

    def test_can_parse_upload_package_with_valid_tarbz2_package(self):
        storage_client = self.app.config['storage_client']
        items_before = self.db.items.count_documents({})

        with tempfile.TemporaryDirectory() as tmpdirname:
            data_path = os.path.join(DATA_PATH, '5p0xMAG_small')
            package_path = os.path.join(tmpdirname, 'package.tar.bz2')
            self.create_package_from_directory(data_path, package_path)
            upload_id = self.upload_package(package_path)
            parse_upload_package(upload_id, self.db, storage_client)

            upload_doc = upload.get(self.db, upload_id, with_default_projection=False)
            self.assertEqual('finished', upload_doc.state)
            self.assertEqual(17, upload_doc.image_count)
            self.assertEqual(0, upload_doc.duplicate_image_count)
            self.assertEqual(0, upload_doc.broken_record_count)
            self.assertCountEqual([], upload_doc.duplicate_filenames)
            self.assertCountEqual([], upload_doc.broken_records)

            items_after = self.db.items.count_documents({})
            self.assertNotEqual(items_before, items_after)

    def test_can_parse_upload_package_with_valid_targz_package(self):
        storage_client = self.app.config['storage_client']
        items_before = self.db.items.count_documents({})

        with tempfile.TemporaryDirectory() as tmpdirname:
            data_path = os.path.join(DATA_PATH, '5p0xMAG_small')
            package_path = os.path.join(tmpdirname, 'package.tar.bz2')
            self.create_package_from_directory(data_path, package_path, compression='gz')
            upload_id = self.upload_package(package_path)
            parse_upload_package(upload_id, self.db, storage_client)

            upload_doc = upload.get(self.db, upload_id, with_default_projection=False)
            self.assertEqual('finished', upload_doc.state)
            self.assertEqual(17, upload_doc.image_count)
            self.assertEqual(0, upload_doc.duplicate_image_count)
            self.assertEqual(0, upload_doc.broken_record_count)
            self.assertCountEqual([], upload_doc.duplicate_filenames)
            self.assertCountEqual([], upload_doc.broken_records)

            items_after = self.db.items.count_documents({})
            self.assertNotEqual(items_before, items_after)

    def test_can_parse_upload_package_with_valid_spc_native_tar_format(self):
        storage_client = self.app.config['storage_client']
        items_before = self.db.items.count_documents({})

        with tempfile.TemporaryDirectory() as tmpdirname:
            data_path = os.path.join(DATA_PATH, '25_feb_upload_example_small')
            package_path = os.path.join(tmpdirname, 'package.tar')
            self.create_package_from_directory(data_path, package_path, compression='')
            upload_id = self.upload_package(package_path)
            parse_upload_package(upload_id, self.db, storage_client)

            upload_doc = upload.get(self.db, upload_id, with_default_projection=False)
            self.assertEqual('finished', upload_doc.state)
            self.assertEqual(8, upload_doc.image_count)
            self.assertEqual(0, upload_doc.duplicate_image_count)
            self.assertEqual(0, upload_doc.broken_record_count)
            self.assertCountEqual([], upload_doc.duplicate_filenames)
            self.assertCountEqual([], upload_doc.broken_records)

            items_after = self.db.items.count_documents({})
            self.assertNotEqual(items_before, items_after)

    def test_cant_parse_upload_package_with_package_with_missing_tsv_file(self):
        storage_client = self.app.config['storage_client']
        items_before = self.db.items.count_documents({})

        with tempfile.TemporaryDirectory() as tmpdirname:
            data_path = os.path.join(DATA_PATH, '5p0xMAG_small_missing_tsv')
            package_path = os.path.join(tmpdirname, 'package.tar.bz2')
            self.create_package_from_directory(data_path, package_path)
            upload_id = self.upload_package(package_path)
            parse_upload_package(upload_id, self.db, storage_client)

            upload_doc = upload.get(self.db, upload_id, with_default_projection=False)
            self.assertEqual('failed', upload_doc.state)

            with self.assertRaises(AttributeError):
                upload_doc.image_count
            with self.assertRaises(AttributeError):
                upload_doc.duplicate_image_count
            with self.assertRaises(AttributeError):
                upload_doc.broken_record_count
            with self.assertRaises(AttributeError):
                upload_doc.duplicate_filenames
            with self.assertRaises(AttributeError):
                upload_doc.broken_records

            items_after = self.db.items.count_documents({})
            self.assertEqual(items_before, items_after)

    def test_cant_parse_upload_package_with_package_with_fake_image(self):
        storage_client = self.app.config['storage_client']
        items_before = self.db.items.count_documents({})

        with tempfile.TemporaryDirectory() as tmpdirname:
            data_path = os.path.join(DATA_PATH, '5p0xMAG_small_fake_image')
            package_path = os.path.join(tmpdirname, 'package.tar.bz2')
            self.create_package_from_directory(data_path, package_path)
            upload_id = self.upload_package(package_path)
            parse_upload_package(upload_id, self.db, storage_client)

            upload_doc = upload.get(self.db, upload_id, with_default_projection=False)
            self.assertEqual('failed', upload_doc.state)

            with self.assertRaises(AttributeError):
                upload_doc.image_count
            with self.assertRaises(AttributeError):
                upload_doc.duplicate_image_count
            with self.assertRaises(AttributeError):
                upload_doc.broken_record_count
            with self.assertRaises(AttributeError):
                upload_doc.duplicate_filenames
            with self.assertRaises(AttributeError):
                upload_doc.broken_records

            items_after = self.db.items.count_documents({})
            self.assertEqual(items_before, items_after)

    def test_cant_parse_upload_package_with_package_with_missing_images(self):
        storage_client = self.app.config['storage_client']
        items_before = self.db.items.count_documents({})

        with tempfile.TemporaryDirectory() as tmpdirname:
            data_path = os.path.join(DATA_PATH, '5p0xMAG_small_missing_images')
            package_path = os.path.join(tmpdirname, 'package.tar.bz2')
            self.create_package_from_directory(data_path, package_path)
            upload_id = self.upload_package(package_path)
            parse_upload_package(upload_id, self.db, storage_client)

            upload_doc = upload.get(self.db, upload_id, with_default_projection=False)
            self.assertEqual('failed', upload_doc.state)

            with self.assertRaises(AttributeError):
                upload_doc.image_count
            with self.assertRaises(AttributeError):
                upload_doc.duplicate_image_count
            with self.assertRaises(AttributeError):
                upload_doc.broken_record_count
            with self.assertRaises(AttributeError):
                upload_doc.duplicate_filenames
            with self.assertRaises(AttributeError):
                upload_doc.broken_records

            items_after = self.db.items.count_documents({})
            self.assertEqual(items_before, items_after)

    def test_cant_parse_upload_package_with_empty_package(self):
        storage_client = self.app.config['storage_client']
        items_before = self.db.items.count_documents({})

        with tempfile.TemporaryDirectory() as tmpdirname, tempfile.TemporaryDirectory() as empty_tmpdirname:
            package_path = os.path.join(tmpdirname, 'package.tar.bz2')
            self.create_package_from_directory(empty_tmpdirname, package_path, arcname='')
            upload_id = self.upload_package(package_path)
            parse_upload_package(upload_id, self.db, storage_client)

            upload_doc = upload.get(self.db, upload_id, with_default_projection=False)
            self.assertEqual('failed', upload_doc.state)

            with self.assertRaises(AttributeError):
                upload_doc.image_count
            with self.assertRaises(AttributeError):
                upload_doc.duplicate_image_count
            with self.assertRaises(AttributeError):
                upload_doc.broken_record_count
            with self.assertRaises(AttributeError):
                upload_doc.duplicate_filenames
            with self.assertRaises(AttributeError):
                upload_doc.broken_records

            items_after = self.db.items.count_documents({})
            self.assertEqual(items_before, items_after)

    def test_cant_parse_upload_package_with_package_that_is_just_a_file(self):
        storage_client = self.app.config['storage_client']
        items_before = self.db.items.count_documents({})

        data_path = os.path.join(DATA_PATH, '5p0xMAG_small', 'features.tsv')
        upload_id = self.upload_package(data_path)
        parse_upload_package(upload_id, self.db, storage_client)

        upload_doc = upload.get(self.db, upload_id, with_default_projection=False)
        self.assertEqual('failed', upload_doc.state)

        with self.assertRaises(AttributeError):
            upload_doc.image_count
        with self.assertRaises(AttributeError):
            upload_doc.duplicate_image_count
        with self.assertRaises(AttributeError):
            upload_doc.broken_record_count
        with self.assertRaises(AttributeError):
            upload_doc.duplicate_filenames
        with self.assertRaises(AttributeError):
            upload_doc.broken_records

        items_after = self.db.items.count_documents({})
        self.assertEqual(items_before, items_after)

    def test_cant_parse_upload_package_with_package_with_empty_tsv_file_and_no_images(self):
        storage_client = self.app.config['storage_client']
        items_before = self.db.items.count_documents({})

        with tempfile.TemporaryDirectory() as tmpdirname:
            data_path = os.path.join(DATA_PATH, '5p0xMAG_small_empty_tsv_no_images')
            package_path = os.path.join(tmpdirname, 'package.tar.bz2')
            self.create_package_from_directory(data_path, package_path)
            upload_id = self.upload_package(package_path)
            parse_upload_package(upload_id, self.db, storage_client)

            upload_doc = upload.get(self.db, upload_id, with_default_projection=False)
            self.assertEqual('failed', upload_doc.state)

            with self.assertRaises(AttributeError):
                upload_doc.image_count
            with self.assertRaises(AttributeError):
                upload_doc.duplicate_image_count
            with self.assertRaises(AttributeError):
                upload_doc.broken_record_count
            with self.assertRaises(AttributeError):
                upload_doc.duplicate_filenames
            with self.assertRaises(AttributeError):
                upload_doc.broken_records

            items_after = self.db.items.count_documents({})
            self.assertEqual(items_before, items_after)

    def test_can_parse_upload_package_with_duplicates_only(self):
        storage_client = self.app.config['storage_client']
        items_before = self.db.items.count_documents({})

        with tempfile.TemporaryDirectory() as tmpdirname:
            data_path = os.path.join(DATA_PATH, '5p0xMAG_small')
            package_path = os.path.join(tmpdirname, 'package.tar.bz2')
            self.create_package_from_directory(data_path, package_path)
            upload_id = self.upload_package(package_path)
            parse_upload_package(upload_id, self.db, storage_client)

            upload_doc = upload.get(self.db, upload_id, with_default_projection=False)
            self.assertEqual('finished', upload_doc.state)
            self.assertEqual(17, upload_doc.image_count)
            self.assertEqual(0, upload_doc.duplicate_image_count)
            self.assertEqual(0, upload_doc.broken_record_count)
            self.assertCountEqual([], upload_doc.duplicate_filenames)
            self.assertCountEqual([], upload_doc.broken_records)

            items_after = self.db.items.count_documents({})
            self.assertNotEqual(items_before, items_after)

        items_inbeetween = self.db.items.count_documents({})

        with tempfile.TemporaryDirectory() as tmpdirname:
            data_path = os.path.join(DATA_PATH, '5p0xMAG_3_entries')
            package_path = os.path.join(tmpdirname, 'package.tar.bz2')
            self.create_package_from_directory(data_path, package_path)
            upload_id = self.upload_package(package_path)
            parse_upload_package(upload_id, self.db, storage_client)

            upload_doc = upload.get(self.db, upload_id, with_default_projection=False)
            self.assertEqual('finished', upload_doc.state)
            self.assertEqual(3, upload_doc.image_count)
            self.assertEqual(3, upload_doc.duplicate_image_count)
            self.assertEqual(0, upload_doc.broken_record_count)
            self.assertCountEqual([
                'SPC-EAWAG-5P0X-1543968085030435-9650530338104-000049-002-2838-1090-48-32.jpeg',
                'SPC-EAWAG-5P0X-1543968169050193-9650614345087-000889-004-2636-0-100-128.jpeg',
                'SPC-EAWAG-5P0X-1543968172024020-9650617345336-000919-002-1364-290-64-72.jpeg'
            ], upload_doc.duplicate_filenames)
            self.assertCountEqual([], upload_doc.broken_records)

            items_after = self.db.items.count_documents({})
            self.assertNotEqual(items_before, items_after)
            self.assertEqual(items_inbeetween, items_after)

    def test_can_parse_upload_package_with_some_duplicates(self):
        storage_client = self.app.config['storage_client']
        items_before = self.db.items.count_documents({})

        with tempfile.TemporaryDirectory() as tmpdirname:
            data_path = os.path.join(DATA_PATH, '5p0xMAG_small')
            package_path = os.path.join(tmpdirname, 'package.tar.bz2')
            self.create_package_from_directory(data_path, package_path)
            upload_id = self.upload_package(package_path)
            parse_upload_package(upload_id, self.db, storage_client)

            upload_doc = upload.get(self.db, upload_id, with_default_projection=False)
            self.assertEqual('finished', upload_doc.state)
            self.assertEqual(17, upload_doc.image_count)
            self.assertEqual(0, upload_doc.duplicate_image_count)
            self.assertEqual(0, upload_doc.broken_record_count)
            self.assertCountEqual([], upload_doc.duplicate_filenames)
            self.assertCountEqual([], upload_doc.broken_records)

            items_after = self.db.items.count_documents({})
            self.assertNotEqual(items_before, items_after)

        items_inbeetween = self.db.items.count_documents({})

        with tempfile.TemporaryDirectory() as tmpdirname:
            data_path = os.path.join(DATA_PATH, '5p0xMAG_small_2_duplicates')
            package_path = os.path.join(tmpdirname, 'package.tar.bz2')
            self.create_package_from_directory(data_path, package_path)
            upload_id = self.upload_package(package_path)
            parse_upload_package(upload_id, self.db, storage_client)

            upload_doc = upload.get(self.db, upload_id, with_default_projection=False)
            self.assertEqual('finished', upload_doc.state)
            self.assertEqual(7, upload_doc.image_count)
            self.assertEqual(2, upload_doc.duplicate_image_count)
            self.assertEqual(0, upload_doc.broken_record_count)
            self.assertCountEqual([
                'SPC-EAWAG-5P0X-1543968111037290-9650556340265-000309-002-3712-0-52-40.jpeg',
                'SPC-EAWAG-5P0X-1543968114038057-9650559340515-000339-001-3536-32-68-92.jpeg'
            ], upload_doc.duplicate_filenames)
            self.assertCountEqual([], upload_doc.broken_records)

            items_after = self.db.items.count_documents({})
            self.assertNotEqual(items_before, items_after)
            self.assertNotEqual(items_inbeetween, items_after)

    def test_can_parse_upload_package_with_duplicated_tsv_entries(self):
        storage_client = self.app.config['storage_client']
        items_before = self.db.items.count_documents({})

        with tempfile.TemporaryDirectory() as tmpdirname:
            data_path = os.path.join(DATA_PATH, '5p0xMAG_small_with_tsv_duplicates')
            package_path = os.path.join(tmpdirname, 'package.tar.bz2')
            self.create_package_from_directory(data_path, package_path)
            upload_id = self.upload_package(package_path)
            parse_upload_package(upload_id, self.db, storage_client)

            upload_doc = upload.get(self.db, upload_id, with_default_projection=False)
            self.assertEqual('finished', upload_doc.state)
            self.assertEqual(19, upload_doc.image_count)
            self.assertEqual(2, upload_doc.duplicate_image_count)
            self.assertEqual(0, upload_doc.broken_record_count)
            self.assertCountEqual([
                'SPC-EAWAG-5P0X-1543968141051783-9650586342759-000609-002-0-2088-32-84.jpeg',
                'SPC-EAWAG-5P0X-1543968092032969-9650537338686-000119-003-2132-1914-48-48.jpeg'
            ], upload_doc.duplicate_filenames)
            self.assertCountEqual([], upload_doc.broken_records)

            items_after = self.db.items.count_documents({})
            self.assertNotEqual(items_before, items_after)

    def test_can_parse_upload_package_with_duplicated_fields_filenames_in_tsv(self):
        storage_client = self.app.config['storage_client']
        items_before = self.db.items.count_documents({})

        with tempfile.TemporaryDirectory() as tmpdirname:
            data_path = os.path.join(DATA_PATH, '5p0xMAG_small_with_tsv_duplicated_filenames')
            package_path = os.path.join(tmpdirname, 'package.tar.bz2')
            self.create_package_from_directory(data_path, package_path)
            upload_id = self.upload_package(package_path)
            parse_upload_package(upload_id, self.db, storage_client)

            upload_doc = upload.get(self.db, upload_id, with_default_projection=False)
            self.assertEqual('finished', upload_doc.state)
            self.assertEqual(19, upload_doc.image_count)
            self.assertEqual(2, upload_doc.duplicate_image_count)
            self.assertEqual(0, upload_doc.broken_record_count)
            self.assertCountEqual([
                'SPC-EAWAG-5P0X-1543968141051783-9650586342759-000609-002-0-2088-32-84.jpeg',
                'SPC-EAWAG-5P0X-1543968092032969-9650537338686-000119-003-2132-1914-48-48.jpeg'
            ], upload_doc.duplicate_filenames)
            self.assertCountEqual([], upload_doc.broken_records)

            items_after = self.db.items.count_documents({})
            self.assertNotEqual(items_before, items_after)
            self.assertEqual(items_after - items_before, upload_doc.image_count - upload_doc.duplicate_image_count)

    def test_can_parse_upload_package_with_some_duplicates_and_duplicated_tsv_entries(self):
        storage_client = self.app.config['storage_client']
        items_before = self.db.items.count_documents({})

        with tempfile.TemporaryDirectory() as tmpdirname:
            data_path = os.path.join(DATA_PATH, '5p0xMAG_small')
            package_path = os.path.join(tmpdirname, 'package.tar.bz2')
            self.create_package_from_directory(data_path, package_path)
            upload_id = self.upload_package(package_path)
            parse_upload_package(upload_id, self.db, storage_client)

            upload_doc = upload.get(self.db, upload_id, with_default_projection=False)
            self.assertEqual('finished', upload_doc.state)
            self.assertEqual(17, upload_doc.image_count)
            self.assertEqual(0, upload_doc.duplicate_image_count)
            self.assertEqual(0, upload_doc.broken_record_count)
            self.assertCountEqual([], upload_doc.duplicate_filenames)
            self.assertCountEqual([], upload_doc.broken_records)

            items_after = self.db.items.count_documents({})
            self.assertNotEqual(items_before, items_after)

        items_inbeetween = self.db.items.count_documents({})

        with tempfile.TemporaryDirectory() as tmpdirname:
            data_path = os.path.join(DATA_PATH, '5p0xMAG_small_2_duplicates_and_tsv_duplicates')
            package_path = os.path.join(tmpdirname, 'package.tar.bz2')
            self.create_package_from_directory(data_path, package_path)
            upload_id = self.upload_package(package_path)
            parse_upload_package(upload_id, self.db, storage_client)

            upload_doc = upload.get(self.db, upload_id, with_default_projection=False)
            self.assertEqual('finished', upload_doc.state)
            self.assertEqual(9, upload_doc.image_count)
            self.assertEqual(4, upload_doc.duplicate_image_count)
            self.assertEqual(0, upload_doc.broken_record_count)
            self.assertCountEqual([
                'SPC-EAWAG-5P0X-1543968111037290-9650556340265-000309-002-3712-0-52-40.jpeg',
                'SPC-EAWAG-5P0X-1543968111037290-9650556340265-000309-002-3712-0-52-40.jpeg',
                'SPC-EAWAG-5P0X-1543968114038057-9650559340515-000339-001-3536-32-68-92.jpeg',
                'SPC-EAWAG-5P0X-1543968114038057-9650559340515-000339-001-3536-32-68-92.jpeg'
            ], upload_doc.duplicate_filenames)
            self.assertCountEqual([], upload_doc.broken_records)

            items_after = self.db.items.count_documents({})
            self.assertNotEqual(items_before, items_after)
            self.assertNotEqual(items_inbeetween, items_after)

    def test_can_parse_upload_package_with_some_fields_as_infs_or_nans(self):
        storage_client = self.app.config['storage_client']
        items_before = self.db.items.count_documents({})

        with tempfile.TemporaryDirectory() as tmpdirname:
            data_path = os.path.join(DATA_PATH, '5p0xMAG_small_with_infs_and_nans')
            package_path = os.path.join(tmpdirname, 'package.tar.bz2')
            self.create_package_from_directory(data_path, package_path)
            upload_id = self.upload_package(package_path)
            parse_upload_package(upload_id, self.db, storage_client)

            upload_doc = upload.get(self.db, upload_id, with_default_projection=False)
            self.assertEqual('finished', upload_doc.state)
            self.assertEqual(17, upload_doc.image_count)
            self.assertEqual(0, upload_doc.duplicate_image_count)
            self.assertEqual(2, upload_doc.broken_record_count)
            self.assertCountEqual([], upload_doc.duplicate_filenames)
            self.assertCountEqual(['SPC-EAWAG-5P0X-1543968157067352-9650602344089-000769-002-3546-2354-48-48.jpeg',
                                   'SPC-EAWAG-5P0X-1543968114038057-9650559340515-000339-001-3536-32-68-92.jpeg'],
                                  upload_doc.broken_records)

            items_after = self.db.items.count_documents({})
            self.assertNotEqual(items_before, items_after)

    def test_can_parse_upload_package_with_some_fields_missing(self):
        storage_client = self.app.config['storage_client']
        items_before = self.db.items.count_documents({})

        with tempfile.TemporaryDirectory() as tmpdirname:
            data_path = os.path.join(DATA_PATH, '5p0xMAG_small_with_missing_fields')
            package_path = os.path.join(tmpdirname, 'package.tar.bz2')
            self.create_package_from_directory(data_path, package_path)
            upload_id = self.upload_package(package_path)
            parse_upload_package(upload_id, self.db, storage_client)

            upload_doc = upload.get(self.db, upload_id, with_default_projection=False)
            self.assertEqual('finished', upload_doc.state)
            self.assertEqual(17, upload_doc.image_count)
            self.assertEqual(0, upload_doc.duplicate_image_count)
            self.assertEqual(1, upload_doc.broken_record_count)
            self.assertCountEqual([], upload_doc.duplicate_filenames)
            self.assertCountEqual(['SPC-EAWAG-5P0X-1543968111037290-9650556340265-000309-002-3712-0-52-40.jpeg'],
                                  upload_doc.broken_records)

            items_after = self.db.items.count_documents({})
            self.assertNotEqual(items_before, items_after)


if __name__ == '__main__':
    unittest.main()
