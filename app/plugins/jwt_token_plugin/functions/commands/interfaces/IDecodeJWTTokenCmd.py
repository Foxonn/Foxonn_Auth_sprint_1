from app.plugins.jwt_token_plugin.models import JWTTokenModels

__all__ = ['IDecodeJWTTokenCmd']


class IDecodeJWTTokenCmd:
    __slots__ = ()

    def __call__(self, token: str) -> JWTTokenModels:
        raise NotImplementedError()
