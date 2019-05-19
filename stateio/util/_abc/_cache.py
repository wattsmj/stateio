#  Abstracts state caching from NAStateIO

from abc import ABCMeta, abstractmethod


class NAAbstractStateCache(object):

    __metaclass__ = ABCMeta

    def __init__(self):
        self._cache = {}

    @abstractmethod
    def _has_attribute(self, key):
        raise NotImplementedError

    @abstractmethod
    def _get_attribute(self, key):
        raise NotImplementedError

    @abstractmethod
    def _store_attribute(self, key, value):
        raise NotImplementedError

    @abstractmethod
    def _delete_attribute(self, key):
        raise NotImplementedError

    def has_attribute(self, key, **kwargs):
        return self._has_attribute(key, **kwargs)

    def get_attribute(self, key, **kwargs):
        return self._get_attribute(key, **kwargs)

    def store_attribute(self, key, value, **kwargs):
        if 'override' in kwargs:
            override = kwargs['override']
        else:
            # Default value is False
            override = False

        # Cannot override existing attribute
        if self.has_attribute(key) and override is False:
            return ValueError('Key is present and overide is False')

        return self._store_attribute(key, value)

    def delete_attribute(self, key, **kwargs):
        return self._delete_attribute(key)
