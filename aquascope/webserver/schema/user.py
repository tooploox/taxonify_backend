from marshmallow import fields
from marshmallow.validate import Regexp

from aquascope.webserver.schema.custom_schema import CustomSchema


class UserSchema(CustomSchema):
    username = fields.String(required=True)
    password = fields.String(required=True)


class NewUserSchema(CustomSchema):
    username = fields.String(allow_none=False, required=True,
                             validate=Regexp('^[a-zA-Z0-9.]{1,64}$', 0,
                                             'Username is invalid'))
