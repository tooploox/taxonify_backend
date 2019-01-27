from marshmallow import Schema, fields


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
