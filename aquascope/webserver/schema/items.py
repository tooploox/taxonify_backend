from marshmallow import Schema, fields

from aquascope.webserver.schema.custom_fields import List, CustomBoolean


class PostItemSchema(Schema):

    id = fields.String(data_key='_id', attribute='_id', required=True)
    filename = fields.String(required=True)
    extension = fields.String(required=True)
    group_id = fields.String(required=True)

    empire = fields.String(required=True)
    kingdom = fields.String(required=True)
    phylum = fields.String(required=True)
    klass = fields.String(data_key='class', attribute='class', required=True)
    order = fields.String(required=True)
    family = fields.String(required=True)
    genus = fields.String(required=True)
    species = fields.String(required=True)

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
    empire = fields.String(required=False)
    kingdom = fields.String(required=False)
    phylum = fields.String(required=False)
    klass = fields.String(data_key='class', attribute='class', required=False)
    order = fields.String(required=False)
    family = fields.String(required=False)
    genus = fields.String(required=False)
    species = fields.String(required=False)
    filename = fields.String(required=False)

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
