__all__ = ['BearerTokenNotFoundError']


class BearerTokenNotFoundError(BaseException):
    def __init__(self, *args: object) -> None:
        msg = 'Bearer token not found.'
        super().__init__(msg)
