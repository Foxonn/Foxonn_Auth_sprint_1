__all__ = ['UserNotFoundError']


class UserNotFoundError(Exception):
    def __init__(self, *args: object) -> None:
        msg = 'User not found.'
        super().__init__(msg)
