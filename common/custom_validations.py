class CustomExceptions(Exception):
    def __init__(self, msg, code):
        self.Error = msg
        self.Code = code


class NullValue(CustomExceptions):
    pass


class AlreadyExist(CustomExceptions):
    pass


class InternalError(CustomExceptions):
    pass


class NotFound(CustomExceptions):
    pass
