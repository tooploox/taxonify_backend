from marshmallow import fields

from aquascope.webserver.schema.custom_schema import CustomSchema

class UserSchema(CustomSchema):
    username = fields.String(required=True)
    password = fields.String(required=True)
