class NetworkError(Exception):
    def __init__(self, message):
        super().__init__(message)


class WebContentNull(Exception):
    def __init__(self, message):
        super().__init__(message)


class NeedCaptcha(Exception):
    def __init__(self, message):
        super().__init__(message)


class WebContentUnintelligible(Exception):
    def __init__(self, message):
        super().__init__(message)


class MissingArg(Exception):
    def __init__(self, message):
        super().__init__(message)


class ZmHttpProxyError(Exception):
    def __init__(self, message):
        super().__init__(message)