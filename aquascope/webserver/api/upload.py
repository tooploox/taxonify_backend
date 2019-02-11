from flask import current_app as app, request
from flask_jwt_extended import jwt_required
from flask_restful import Resource

import aquascope.webserver.data_access.db.upload as upload
import aquascope.webserver.data_access.storage.blob as blob


class Upload(Resource):
    @jwt_required
    def put(self, filename):
        storage_client = app.config['storage_client']

        container_name = blob.group_id_to_container_name('upload')
        if not blob.exists(storage_client, container_name):
            blob.create_container(storage_client, container_name)

        db = app.config['db']
        upload_doc = upload.create(db, filename)
        blob_filename = str(upload_doc.inserted_id)
        blob_meta = dict(filename=filename)
        blob.create_blob_from_stream(storage_client, container_name, blob_filename, request.stream,
                                     blob_meta)
        upload.update_state(db, blob_filename, 'uploaded')

        celery_app = app.config['celery']
        celery_app.send_task('aquascope.tasks.upload_postprocess.parse_upload',
                             args=[blob_filename])

        return '', 204


class UploadList(Resource):
    @jwt_required
    def get(self):
        db = app.config['db']
        docs = upload.find(db)
        return [doc.serializable() for doc in docs]
