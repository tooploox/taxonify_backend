from flask import current_app as app, request
from flask_jwt_extended import jwt_required
from flask_restful import Resource

import aquascope.webserver.data_access.storage.blob as blob


class Upload(Resource):
    @jwt_required
    def put(self, filename):
        storage_client = app.config['storage_client']

        container_name = blob.group_id_to_container_name('upload')
        if not blob.exists(storage_client, container_name):
            blob.create_container(storage_client, container_name)

        blob.create_blob_from_stream(storage_client, container_name, filename, request.stream)
