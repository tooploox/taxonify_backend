from marshmallow import fields
from marshmallow.validate import Range

from aquascope.webserver.data_access.db.items import (ADDITIONAL_ATTRIBUTES_FIELDS, PRIMARY_MORPHOMETRIC_FIELDS,
                                                      TAXONOMY_FIELDS, ANNOTABLE_FIELDS)
from aquascope.webserver.schema.custom_fields import (List, NullableBoolean,
                                                      LowercaseNullableString, NullableString)
from aquascope.webserver.schema.custom_schema import (CustomSchema, FormattedValidationError)


PostItemSchema = type('PostItemSchema', (CustomSchema,), {
    '_id': fields.String(required=True),
    'filename': fields.String(required=True, allow_none=True),
    'extension': LowercaseNullableString(required=True, allow_none=True),
    'group_id': LowercaseNullableString(required=True, allow_none=True),
    'acquisition_time': fields.String(required=True),
    'image_width': fields.Integer(required=True),
    'image_height': fields.Integer(required=True),
    **({k: LowercaseNullableString(required=True, allow_none=True) for k in TAXONOMY_FIELDS}),
    **({k: fields.Boolean(allow_none=True, required=True) for k in ADDITIONAL_ATTRIBUTES_FIELDS}),
    **({k: fields.Float(allow_none=False, required=True) for k in PRIMARY_MORPHOMETRIC_FIELDS}),
    **({f'{k}_modified_by': NullableString(required=True, allow_none=True) for k in ANNOTABLE_FIELDS})
})


class PostItemsUpdateSchema(CustomSchema):
    current = fields.Nested(PostItemSchema, required=True)
    update = fields.Nested(PostItemSchema, required=True)

    def load(self, json_data, many=None, partial=None, unknown=None):
        if not json_data:
            raise FormattedValidationError(dict(length='Length must be non-zero'))

        return super().load(json_data, many, partial, unknown)


GetItemsSchema = type('GetItemsSchema', (CustomSchema,), {
    'filename': NullableString(required=False, allow_none=True),
    'acquisition_time_start': fields.DateTime(required=False),
    'acquisition_time_end': fields.DateTime(required=False),
    **({k: LowercaseNullableString(required=False, allow_none=True) for k in TAXONOMY_FIELDS}),
    **({k: List(NullableBoolean(allow_none=True), allow_none=True, required=False) for k in ADDITIONAL_ATTRIBUTES_FIELDS}),

})


class GetPagedItemsSchema(GetItemsSchema):
    continuation_token = fields.Integer(required=False, allow_none=False, validate=Range(1))
