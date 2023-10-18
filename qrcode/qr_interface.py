from abc import abstractmethod, ABCMeta


class QrCodeReader(metaclass=ABCMeta):
    def __init__(self, label=None, controller=None):
        pass

    @abstractmethod
    def startCapture(self):
        pass

    @abstractmethod
    def onClose(self):
        pass
