from flask import current_app as app
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from aquascope.data_processing.export import export_items
from aquascope.webserver.data_access.db.items import paged_find_items
from aquascope.webserver.schema.custom_schema import FormattedValidationError
from aquascope.webserver.schema.export import ExportSchema


class Export(Resource):
    @jwt_required
    def get(self):
        schema = ExportSchema()
        try:
            args = schema.load(request.args)
        except FormattedValidationError as e:
            return e.formatted_messages, 400

        db = app.config['db']
        storage_client = app.config['storage_client']

        limit = args.pop('limit', 0)
        items = list(paged_find_items(db, limit, 1, with_default_projection=False,
                                      serializable=True, **args))

        exported_items_url = export_items(items, storage_client)
        return dict(url=exported_items_url)
