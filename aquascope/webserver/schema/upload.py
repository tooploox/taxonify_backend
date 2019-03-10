from marshmallow import fields

from aquascope.webserver.schema.custom_fields import List
from aquascope.webserver.schema.custom_schema import CustomSchema


class UploadTagsSchema(CustomSchema):
    tags = List(fields.String(required=True, allow_none=False), required=True, allow_none=False)
