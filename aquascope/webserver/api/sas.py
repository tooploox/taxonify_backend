from flask import current_app as app
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from aquascope.webserver.data_access.conversions import GROUP_ID_TO_CONTAINER, group_id_to_container_name
from aquascope.webserver.data_access.storage.blob import generate_container_download_sas


class Sas(Resource):
    @jwt_required
    def get(self):
        parser = reqparse.RequestParser()

        allowed_destinations = tuple(GROUP_ID_TO_CONTAINER.keys())
        parser.add_argument('destination', type=str, required=True,
                            choices=allowed_destinations)
        args = parser.parse_args(strict=True)

        group_id = args['destination']
        container_name = group_id_to_container_name(group_id)
        storage_client = app.config['storage_client']
        return dict(token=generate_container_download_sas(storage_client, container_name))
