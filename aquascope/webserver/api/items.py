import json

from bson.json_util import dumps
from flask import current_app as app
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse, inputs

from aquascope.webserver.data_access.items import find_items

# Sample json document
# {
#     "filename": "img2353.jpeg",
#     "empire": "prokaryota",
#     "kingdom": "Bacteria",
#     "phylum": "Cyanobacteria",
#     "class": "Cyanophyceae",
#     "order": "Nostocales",
#     "family": "Nostocaceae",
#     "genus": "Anabaena",
#     "species": "sp",
#     "dividing": false,
#     "dead": false,
#     "with_epiphytes": false,
#     "broken": false,
#     "colony": false,
#     "eating": false,
#     "multiple species": false,
#     "cropped": false,
#     "male": null,
#     "female": null,
#     "juvenile": null,
#     "adult": null,
#     "with_eggs": null
# },


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

        parser.add_argument('dividing', type=str, required=False, store_missing=False, action='append')
        parser.add_argument('dead', type=str, required=False, store_missing=False, action='append')
        parser.add_argument('with_ephiphytes', type=str, required=False, store_missing=False, action='append')
        parser.add_argument('broken', type=str, required=False, store_missing=False, action='append')
        parser.add_argument('colony', type=str, required=False, store_missing=False, action='append')
        parser.add_argument('multiple_species', type=str, required=False, store_missing=False, action='append')
        parser.add_argument('cropped', type=str, required=False, store_missing=False, action='append')
        parser.add_argument('male', type=str, required=False, store_missing=False, action='append')
        parser.add_argument('female', type=str, required=False, store_missing=False, action='append')
        parser.add_argument('juvenile', type=str, required=False, store_missing=False, action='append')
        parser.add_argument('adult', type=str, required=False, store_missing=False, action='append')
        parser.add_argument('with_eggs', type=str, required=False, store_missing=False, action='append')
        args = parser.parse_args()
        items = find_items(**args)

        # we need to serialize and deserialize it
        dump = dumps(items)
        return json.loads(dump)
