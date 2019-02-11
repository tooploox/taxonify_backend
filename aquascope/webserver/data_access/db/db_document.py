import copy


class DbDocument(object):
    def __init__(self, obj):
        for k, v in obj.items():
            if isinstance(v, dict):
                setattr(self, k, DbDocument(v))
            else:
                setattr(self, k, v)

    def __getitem__(self, key):
        return self.__dict__[key]

    def __repr__(self):
        return '{%s}' % str(', '.join('%s : %s' % (k, repr(v)) for
                                      (k, v) in self.__dict__.items()))

    @staticmethod
    def from_db_data(db_data):
        return DbDocument(copy.deepcopy(db_data))

    def get_dict(self):
        return copy.deepcopy(self.__dict__)
