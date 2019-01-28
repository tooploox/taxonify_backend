from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from marshmallow import ValidationError


from aquascope.webserver.data_access.db import Item, bulk_replace, find_items
from aquascope.webserver.data_access.storage.blob import get_urls_for_items
from aquascope.webserver.schema.items import PostItemsUpdateSchema, GetItemsSchema


class Items(Resource):
    @jwt_required
    def get(self):
        schema = GetItemsSchema()
        try:
            args = schema.load(request.args)
        except ValidationError as e:
            return e.messages, 400

        items = list(find_items(**args))
        urls = get_urls_for_items(items)

        return {
            'items': [item.serializable() for item in items],
            'urls': urls
        }

    @jwt_required
    def post(self):
        json_data = request.get_json(force=True)

        schema = PostItemsUpdateSchema(many=True)

        try:
            json_data = schema.load(json_data)
        except ValidationError as e:
            return e.messages, 400

        update_pairs = [
            (Item.from_request(elem['current']), Item.from_request(elem['update'])) for elem in json_data
        ]
        result = bulk_replace(update_pairs)
        return {
            "matched": result.matched_count,
            "modified": result.modified_count
        }
