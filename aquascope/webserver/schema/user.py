from marshmallow import Schema, fields


class GetUserLoginSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)
