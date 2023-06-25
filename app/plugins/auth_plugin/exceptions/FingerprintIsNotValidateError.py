__all__ = ['FingerprintIsNotValidateError']


class FingerprintIsNotValidateError(Exception):
    def __init__(self, *args: object) -> None:
        msg = 'The authenticity of the token key could not be confirmed.'
        super().__init__(msg)
