from collections import abc

import copy
import yaml


def data_merge(a, b):
    a = copy.deepcopy(a)
    if isinstance(a, abc.Mapping):
        if not isinstance(b, abc.Mapping):
            raise TypeError('cannot merge {} into a dictionary'.format(b))
        for k in b:
            try:
                a[k] = data_merge(a[k], b[k])
            except KeyError:
                a[k] = b[k]
    else:
        a = b
    return a


class ConfigDict:
    class NoKey(KeyError):
        """Raised when someone accesses an attribute that wasn't set.
        """
        pass

    def __init__(self, data):
        self.data = data

    def keys(self):
        return self.data.keys()

    def __getitem__(self, key):
        return self.data[key]

    def __getattr__(self, k):
        try:
            v = self.data[k]
        except KeyError:
            raise self.NoKey(k)

        if isinstance(v, abc.Mapping):
            v = ConfigDict(v)

        return v


class Config(ConfigDict):

    def __init__(self, path):
        with open(path) as fi:
            loaded = yaml.load(fi)

        merged = copy.deepcopy(self.DEFAULT)
        merged = data_merge(merged, loaded)

        super(Config, self).__init__(merged)

    DEFAULT = dict()
