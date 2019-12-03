from bson.errors import InvalidId
from flask import current_app as app, request
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from aquascope.webserver.data_access.db import upload
from aquascope.webserver.data_access.util import upload_package_from_stream
from aquascope.webserver.schema.custom_schema import FormattedValidationError
from aquascope.webserver.schema.upload import UploadTagsSchema


def invalid_request():
    return dict(message='No such upload.'), 400


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

        return dict(_id=upload_id), 200


class UploadTags(Resource):
    @jwt_required
    def post(self, upload_id):
        json_data = request.get_json(force=True, silent=True)
        schema = UploadTagsSchema()

        try:
            json_data = schema.load(json_data)
        except FormattedValidationError as e:
            return e.formatted_messages, 400

        db_client = app.config['db_client']
        db = app.config['db']

        try:
            res = upload.update_tags(db_client, db, upload_id, json_data['tags'])
        except InvalidId:
            return invalid_request()

        if not res.matched_count:
            return invalid_request()
        else:
            return None, 204


class UploadGet(Resource):
    @jwt_required
    def get(self, upload_id):
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
        return [doc.serializable(shallow=True) for doc in docs][::-1]
