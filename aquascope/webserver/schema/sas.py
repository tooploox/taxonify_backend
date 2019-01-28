from marshmallow import Schema, fields, validate

from aquascope.webserver.data_access.conversions import GROUP_ID_TO_CONTAINER


class GetSasSchema(Schema):
    destination = fields.String(validate=validate.OneOf(tuple(GROUP_ID_TO_CONTAINER.keys())),
                                required=True)
