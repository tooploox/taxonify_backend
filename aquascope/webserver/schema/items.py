from marshmallow import Schema, fields

from aquascope.webserver.schema.custom_fields import (List, CustomBoolean,
                                                      LowercaseString)


class PostItemSchema(Schema):

    id = fields.String(data_key='_id', attribute='_id', required=True)
    filename = fields.String(required=True)
    extension = LowercaseString(required=True)
    group_id = LowercaseString(required=True)

    empire = LowercaseString(required=True)
    kingdom = LowercaseString(required=True)
    phylum = LowercaseString(required=True)
    class_field = LowercaseString(data_key='class', attribute='class', required=True)
    order = LowercaseString(required=True)
    family = LowercaseString(required=True)
    genus = LowercaseString(required=True)
    species = LowercaseString(required=True)

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

    acquisition_time = fields.String(allow_none=True, required=True)
    image_width = fields.Integer(required=True)
    image_height = fields.Integer(required=True)


class PostItemsUpdateSchema(Schema):
    current = fields.Nested(PostItemSchema, required=True)
    update = fields.Nested(PostItemSchema, required=True)


class GetItemsSchema(Schema):
    empire = LowercaseString(required=False)
    kingdom = LowercaseString(required=False)
    phylum = LowercaseString(required=False)
    class_field = LowercaseString(data_key='class', attribute='class', required=False)
    order = LowercaseString(required=False)
    family = LowercaseString(required=False)
    genus = LowercaseString(required=False)
    species = LowercaseString(required=False)
    filename = LowercaseString(required=False)

    acquisition_time_start = fields.DateTime(required=False)
    acquisition_time_end = fields.DateTime(required=False)

    eating = List(CustomBoolean(allow_none=True), allow_none=True, required=False)
    dividng = List(CustomBoolean(allow_none=True), allow_none=True, required=False)
    dead = List(CustomBoolean(allow_none=True), allow_none=True, required=False)
    with_epiphytes = List(CustomBoolean(allow_none=True), allow_none=True, required=False)
    broken = List(CustomBoolean(allow_none=True), allow_none=True, required=False)
    colony = List(CustomBoolean(allow_none=True), allow_none=True, required=False)
    multiple_species = List(CustomBoolean(allow_none=True), allow_none=True, required=False)
    cropped = List(CustomBoolean(allow_none=True), allow_none=True, required=False)
    male = List(CustomBoolean(allow_none=True), allow_none=True, required=False)
    female = List(CustomBoolean(allow_none=True), allow_none=True, required=False)
    juvenile = List(CustomBoolean(allow_none=True), allow_none=True, required=False)
    adult = List(CustomBoolean(allow_none=True), allow_none=True, required=False)
    with_eggs = List(CustomBoolean(allow_none=True), allow_none=True, required=False)
