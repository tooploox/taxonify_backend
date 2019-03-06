from bson.errors import InvalidId
from flask import current_app as app, request
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from aquascope.webserver.data_access.db import upload
from aquascope.webserver.data_access.util import upload_package_from_stream


class UploadPut(Resource):
    @jwt_required
    def put(self, filename):
        storage_client = app.config['storage_client']
        db = app.config['db']

        upload_id = upload_package_from_stream(filename, request.stream, db, storage_client)

        try:
            celery_app = app.config['celery']
            celery_app.send_task('aquascope.tasks.upload_postprocess.parse_upload',
                                 args=[upload_id])
        except ValueError as e:
            app.logger.critical(f'celery connection error: {str(e)}')
            return 'Server connectivity issue', 500

        return None, 204


class UploadGet(Resource):
    @jwt_required
    def get(self, upload_id):
        def invalid_request():
            return dict(message='No such upload.'), 400

        db = app.config['db']
        try:
            doc = upload.get(db, upload_id, with_default_projection=False)
        except InvalidId:
            return invalid_request()

        if doc:
            return doc.serializable(shallow=True)
        else:
            return invalid_request()


class UploadList(Resource):
    @jwt_required
    def get(self):
        db = app.config['db']
        docs = upload.find(db)
        return [doc.serializable(shallow=True) for doc in docs]
