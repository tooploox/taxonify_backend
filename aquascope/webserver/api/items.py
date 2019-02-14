from flask import current_app as app
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource


from aquascope.webserver.data_access.db import Item, bulk_replace, find_items
from aquascope.webserver.data_access.storage.blob import get_urls_for_items_dicts
from aquascope.webserver.schema.items import PostItemsUpdateSchema, GetItemsSchema
from aquascope.webserver.schema.custom_schema import FormattedValidationError


class Items(Resource):
    @jwt_required
    def get(self):
        schema = GetItemsSchema()
        try:
            args = schema.load(request.args)
        except FormattedValidationError as e:
            return e.formatted_messages, 400

        db = app.config['db']
        items = list(find_items(db, with_default_projection=True, serializable=True, **args))
        urls = get_urls_for_items_dicts(items)

        return {
            'items': items,
            'urls': urls
        }

    @jwt_required
    def post(self):
        json_data = request.get_json(force=True)

        schema = PostItemsUpdateSchema(many=True)

        try:
            json_data = schema.load(json_data)
        except FormattedValidationError as e:
            return e.formatted_messages, 400

        update_pairs = [
            (Item.from_request(elem['current']), Item.from_request(elem['update'])) for elem in json_data
        ]

        db = app.config['db']
        result = bulk_replace(db, update_pairs)
        return {
            "matched": result.matched_count,
            "modified": result.modified_count
        }
