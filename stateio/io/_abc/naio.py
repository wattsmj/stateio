from abc import ABCMeta, abstractmethod

class NAIO(object):

    __metaclass__ = ABCMeta
    
    @abstractmethod
    def get_state(self, cmd):
        raise NotImplementedError
