from marshmallow import fields


class List(fields.List):
    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(data, dict) and hasattr(data, 'getlist'):
            value = data.getlist(attr)
        return super()._deserialize(value, attr, data)


class CustomBoolean(fields.Boolean):
    def _deserialize(self, value, attr, data, **kwargs):
        if value == '':
            return None
        return super(CustomBoolean, self)._deserialize(value, attr, data)


class LowercaseString(fields.String):
    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, str):
            value = value.lower()
        return super()._deserialize(value, attr, data)
