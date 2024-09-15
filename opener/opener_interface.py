from abc import abstractmethod, ABCMeta

class OpenerFacade:
 
 @abstractmethod
 def unlock(self, observable=None):
        pass

 @abstractmethod
 def lock(self, observable=None):
        pass