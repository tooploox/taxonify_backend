from marshmallow import fields, ValidationError

from aquascope.webserver.schema.custom_fields import (List, NullableBoolean,
                                                      LowercaseNullableString)
from aquascope.webserver.schema.custom_schema import CustomSchema

class PostItemSchema(CustomSchema):

    id = fields.String(data_key='_id', attribute='_id', required=True)
    filename = fields.String(required=True, allow_none=True)
    extension = LowercaseNullableString(required=True, allow_none=True)
    group_id = LowercaseNullableString(required=True, allow_none=True)

    empire = LowercaseNullableString(required=True, allow_none=True)
    kingdom = LowercaseNullableString(required=True, allow_none=True)
    phylum = LowercaseNullableString(required=True, allow_none=True)
    class_field = LowercaseNullableString(data_key='class', attribute='class', required=True, allow_none=True)
    order = LowercaseNullableString(required=True, allow_none=True)
    family = LowercaseNullableString(required=True, allow_none=True)
    genus = LowercaseNullableString(required=True, allow_none=True)
    species = LowercaseNullableString(required=True, allow_none=True)

    eating = fields.Boolean(allow_none=True, required=True)
    dividing = fields.Boolean(allow_none=True, required=True)
    dead = fields.Boolean(allow_none=True, required=True)
    with_epiphytes = fields.Boolean(allow_none=True, required=True)
    broken = fields.Boolean(allow_none=True, required=True)
    colony = fields.Boolean(allow_none=True, required=True)
    multiple_species = fields.Boolean(allow_none=True, required=True)
    cropped = fields.Boolean(allow_none=True, required=True)
    male = fields.Boolean(allow_none=True, required=True)
    female = fields.Boolean(allow_none=True, required=True)
    juvenile = fields.Boolean(allow_none=True, required=True)
    adult = fields.Boolean(allow_none=True, required=True)
    with_eggs = fields.Boolean(allow_none=True, required=True)

    acquisition_time = fields.String(required=True)
    image_width = fields.Integer(required=True)
    image_height = fields.Integer(required=True)


class PostItemsUpdateSchema(CustomSchema):
    current = fields.Nested(PostItemSchema, required=True)
    update = fields.Nested(PostItemSchema, required=True)

    def load(self, json_data, many=None, partial=None, unknown=None):
        if not json_data:
            raise ValidationError(dict(length='Length must be non-zero'))

        return super().load(json_data, many, partial, unknown)


class GetItemsSchema(CustomSchema):
    empire = LowercaseNullableString(required=False, allow_none=True)
    kingdom = LowercaseNullableString(required=False, allow_none=True)
    phylum = LowercaseNullableString(required=False, allow_none=True)
    class_field = LowercaseNullableString(data_key='class', attribute='class', required=False, allow_none=True)
    order = LowercaseNullableString(required=False, allow_none=True)
    family = LowercaseNullableString(required=False, allow_none=True)
    genus = LowercaseNullableString(required=False, allow_none=True)
    species = LowercaseNullableString(required=False, allow_none=True)
    filename = LowercaseNullableString(required=False, allow_none=True)

    acquisition_time_start = fields.DateTime(required=False)
    acquisition_time_end = fields.DateTime(required=False)

    eating = List(NullableBoolean(allow_none=True), allow_none=True, required=False)
    dividing = List(NullableBoolean(allow_none=True), allow_none=True, required=False)
    dead = List(NullableBoolean(allow_none=True), allow_none=True, required=False)
    with_epiphytes = List(NullableBoolean(allow_none=True), allow_none=True, required=False)
    broken = List(NullableBoolean(allow_none=True), allow_none=True, required=False)
    colony = List(NullableBoolean(allow_none=True), allow_none=True, required=False)
    multiple_species = List(NullableBoolean(allow_none=True), allow_none=True, required=False)
    cropped = List(NullableBoolean(allow_none=True), allow_none=True, required=False)
    male = List(NullableBoolean(allow_none=True), allow_none=True, required=False)
    female = List(NullableBoolean(allow_none=True), allow_none=True, required=False)
    juvenile = List(NullableBoolean(allow_none=True), allow_none=True, required=False)
    adult = List(NullableBoolean(allow_none=True), allow_none=True, required=False)
    with_eggs = List(NullableBoolean(allow_none=True), allow_none=True, required=False)
