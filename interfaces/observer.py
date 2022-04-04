class ConnectionObserver:

    def notifyOnClose(self, observable=None, message=None, exception=None):
        pass

    def notifyOnOpen(self, observable=None, message=None, exception=None):
        pass

    def notifyOnMessage(self, observable=None, message=None, exception=None):
        pass

    def notifyOnError(self, observable=None, message=None, exception=None):
        pass
