class Error(Exception):
    def __init__(self, message):
        self._message = message

    def __str__(self):
        return self._message

class ConnError(Error):
    def __init__(self, message):
        super().__init__(message)

class HTTPError(Error):
    def __init__(self, message):
        super().__init__(message) 
