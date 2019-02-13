
class DbDocument(object):
    def __init__(self, obj):
        o = obj.get_dict() if isinstance(obj, DbDocument) else obj
        for k, v in o.items():
            setattr(self, k, v)

    def __getitem__(self, key):
        return self.__dict__[key]

    def __repr__(self):
        return '{%s}' % str(', '.join('%s : %s' % (k, repr(v)) for
                                      (k, v) in self.__dict__.items()))

    @staticmethod
    def from_db_data(db_data):
        return DbDocument(db_data)

    def get_dict(self):
        return self.__dict__
