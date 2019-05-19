#  Abstracts state caching from NAStateIO

from ._abc import NAAbstractStateCache

class NAStateCache(NAAbstractStateCache):

    def _has_attribute(self, key):
        if key in self._cache:
            return True
        else:
            return False

    def _get_attribute(self, key):
        if self.has_attribute(key):
            return self._cache[key]
        else:
            return None

    def _store_attribute(self, key, value, **kwargs):
        self._cache[key] = value

    def _delete_attribute(self, key):
        try:
            del self._cache[key]
            return True
        except KeyError:
            return False