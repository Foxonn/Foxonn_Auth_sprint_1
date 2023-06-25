__all__ = ['TokenExpiredError']


class TokenExpiredError(BaseException):
    def __init__(self, *args: object) -> None:
        msg = 'Token expired.'
        super().__init__(msg)
