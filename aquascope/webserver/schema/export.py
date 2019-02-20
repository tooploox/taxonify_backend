from marshmallow import fields
from marshmallow.validate import Range

from aquascope.webserver.schema.custom_schema import CustomSchema
from aquascope.webserver.schema.items import GetItemsSchema


class ExportSchema(CustomSchema):
    filter = fields.Nested(GetItemsSchema, required=True)
    limit = fields.Integer(required=False, allow_none=False, validate=Range(1))
