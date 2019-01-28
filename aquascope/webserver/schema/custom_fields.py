from marshmallow import fields


class List(fields.List):
    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(data, dict) and hasattr(data, 'getlist'):
            value = data.getlist(attr)
        return super()._deserialize(value, attr, data)


class NullableString(fields.String):
    def _deserialize(self, value, attr, data, **kwargs):
        if value == '':
            return None
        return super(NullableString, self)._deserialize(value, attr, data)


class NullableBoolean(fields.Boolean):
    def _deserialize(self, value, attr, data, **kwargs):
        if value == '':
            return None
        return super(NullableBoolean, self)._deserialize(value, attr, data)


class LowercaseNullableString(NullableString):
    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, str):
            value = value.lower()
        return super()._deserialize(value, attr, data)
