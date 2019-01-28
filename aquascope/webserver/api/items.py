import dateutil.parser
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from marshmallow import ValidationError


from aquascope.webserver.data_access.db import Item, bulk_replace, find_items
from aquascope.webserver.data_access.storage.blob import get_urls_for_items
from aquascope.webserver.schema.items import PostItemsUpdateSchema


class Items(Resource):
    @jwt_required
    def get(self):
        parser = reqparse.RequestParser()

        parser.add_argument('empire', type=str, required=False, store_missing=False)
        parser.add_argument('kingdom', type=str, required=False, store_missing=False)
        parser.add_argument('phylum', type=str, required=False, store_missing=False)
        parser.add_argument('class', type=str, required=False, store_missing=False)
        parser.add_argument('order', type=str, required=False, store_missing=False)
        parser.add_argument('family', type=str, required=False, store_missing=False)
        parser.add_argument('genus', type=str, required=False, store_missing=False)
        parser.add_argument('species', type=str, required=False, store_missing=False)
        parser.add_argument('filename', type=str, required=False, store_missing=False)

        parser.add_argument('acquisition_time_start', type=str, required=False, store_missing=False)
        parser.add_argument('acquisition_time_end', type=str, required=False, store_missing=False)
        parser.add_argument('eating', type=str, required=False, store_missing=False, action='append')
        parser.add_argument('dividing', type=str, required=False, store_missing=False, action='append')
        parser.add_argument('dead', type=str, required=False, store_missing=False, action='append')
        parser.add_argument('with_epiphytes', type=str, required=False, store_missing=False, action='append')
        parser.add_argument('broken', type=str, required=False, store_missing=False, action='append')
        parser.add_argument('colony', type=str, required=False, store_missing=False, action='append')
        parser.add_argument('multiple_species', type=str, required=False, store_missing=False, action='append')
        parser.add_argument('cropped', type=str, required=False, store_missing=False, action='append')
        parser.add_argument('male', type=str, required=False, store_missing=False, action='append')
        parser.add_argument('female', type=str, required=False, store_missing=False, action='append')
        parser.add_argument('juvenile', type=str, required=False, store_missing=False, action='append')
        parser.add_argument('adult', type=str, required=False, store_missing=False, action='append')
        parser.add_argument('with_eggs', type=str, required=False, store_missing=False, action='append')

        args = parser.parse_args(strict=True)

        if 'acquisition_time_start' in args:
            args['acquisition_time_start'] = dateutil.parser.parse(args['acquisition_time_start'])
        if 'acquisition_time_end' in args:
            args['acquisition_time_end'] = dateutil.parser.parse(args['acquisition_time_end'])

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
