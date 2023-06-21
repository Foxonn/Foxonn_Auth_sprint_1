__all__ = ['TokenNotActiveError']


class TokenNotActiveError(BaseException):
    def __init__(self, *args: object) -> None:
        msg = 'Token not active.'
        super().__init__(msg)
