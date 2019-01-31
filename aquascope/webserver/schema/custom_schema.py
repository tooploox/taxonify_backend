from marshmallow import Schema, ValidationError
from flatten_dict import flatten

SCHEMA = '_schema'

class FormattedValidationError(ValidationError):
    def __init__(self, message, field_name=SCHEMA, data=None, valid_data=None, **kwargs):
        ValidationError.__init__(self, message, field_name, data, valid_data, **kwargs)
        result_list = []
        flat_dict = flatten(self.messages)
        for parameter, errors in flat_dict.items():
            parameter = tuple(str(s) for s in parameter)
            result_list.append({"parameter": '.'.join(parameter), "errors": errors})
        self.formatted_messages = {"messages": result_list}
        print(self.formatted_messages)


class CustomSchema(Schema):
    def handle_error(self, error, data):
        raise FormattedValidationError(message=error.messages, field_name=error.field_name,
                                       data=error.data, valid_data=error.valid_data, **error.kwargs)

