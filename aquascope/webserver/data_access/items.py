from flask import current_app as app
from flask_restful import inputs


def remap_value(value):
    if value == '':
        value = None
    else:
        try:
            value = inputs.boolean(value)
        except ValueError:
            pass

    return value


def find_items(*args, **kwargs):
    query = dict()
    for key, value in kwargs.items():
        if type(value) == list:
            value = [remap_value(val) for val in value]
            query[key] = {
                '$in': value
            }
        else:
            value = remap_value(value)
            query[key] = value

    db = app.config['db']
    return db.items.find(query)
