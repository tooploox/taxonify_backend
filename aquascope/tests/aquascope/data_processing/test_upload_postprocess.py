import os
import tarfile
import tempfile

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

    def test_can_parse_upload_package_with_valid_package(self):
        storage_client = self.app.config['storage_client']
        items_before = self.db.items.count_documents({})

        with tempfile.TemporaryDirectory() as tmpdirname:
            data_path = os.path.join(DATA_PATH, '5p0xMAG_small')
            package_path = os.path.join(tmpdirname, 'package.tar.bz2')
            self.create_package_from_directory(data_path, package_path)
            upload_id = self.upload_package(package_path)
            parse_upload_package(upload_id, self.db, storage_client)

            upload_doc = upload.get(self.db, upload_id)
            self.assertEqual('finished', upload_doc.state)

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

            upload_doc = upload.get(self.db, upload_id)
            self.assertEqual('failed', upload_doc.state)

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

            upload_doc = upload.get(self.db, upload_id)
            self.assertEqual('failed', upload_doc.state)

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

            upload_doc = upload.get(self.db, upload_id)
            self.assertEqual('failed', upload_doc.state)

            items_after = self.db.items.count_documents({})
            self.assertEqual(items_before, items_after)

    def test_cant_parse_upload_package_with_package_that_isnt_tarbz2(self):
        storage_client = self.app.config['storage_client']
        items_before = self.db.items.count_documents({})

        with tempfile.TemporaryDirectory() as tmpdirname:
            data_path = os.path.join(DATA_PATH, '5p0xMAG_small_missing_images')
            package_path = os.path.join(tmpdirname, 'package.tar.bz2')
            self.create_package_from_directory(data_path, package_path, compression='gz')
            upload_id = self.upload_package(package_path)
            parse_upload_package(upload_id, self.db, storage_client)

            upload_doc = upload.get(self.db, upload_id)
            self.assertEqual('failed', upload_doc.state)

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

            upload_doc = upload.get(self.db, upload_id)
            self.assertEqual('failed', upload_doc.state)

            items_after = self.db.items.count_documents({})
            self.assertEqual(items_before, items_after)

    def test_cant_parse_upload_package_with_package_that_is_just_a_file(self):
        storage_client = self.app.config['storage_client']
        items_before = self.db.items.count_documents({})

        data_path = os.path.join(DATA_PATH, '5p0xMAG_small', 'features.tsv')
        upload_id = self.upload_package(data_path)
        parse_upload_package(upload_id, self.db, storage_client)

        upload_doc = upload.get(self.db, upload_id)
        self.assertEqual('failed', upload_doc.state)

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

            upload_doc = upload.get(self.db, upload_id)
            self.assertEqual('failed', upload_doc.state)

            items_after = self.db.items.count_documents({})
            self.assertEqual(items_before, items_after)
