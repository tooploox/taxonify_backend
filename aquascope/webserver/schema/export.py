from marshmallow import fields
from marshmallow.validate import Range

from aquascope.webserver.schema.items import GetItemsSchema


class ExportSchema(GetItemsSchema):
    limit = fields.Integer(required=False, allow_none=False, validate=Range(1))
