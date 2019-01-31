from marshmallow import fields, validate

from aquascope.webserver.data_access.conversions import GROUP_ID_TO_CONTAINER
from aquascope.webserver.schema.custom_schema import CustomSchema


class SasSchema(CustomSchema):
    destination = fields.String(validate=validate.OneOf(tuple(GROUP_ID_TO_CONTAINER.keys())),
                                required=True)
