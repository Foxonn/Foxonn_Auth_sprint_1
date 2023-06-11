from app.models.jwt_token_models import JWTTokenModels

__all__ = ['IDecodeJWTTokenCmd']


class IDecodeJWTTokenCmd:
    __slots__ = ()

    def __call__(self, token: str) -> JWTTokenModels:
        raise NotImplementedError()
