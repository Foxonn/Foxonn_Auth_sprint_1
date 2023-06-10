import typing as t

from app.models.jwt_token_models import JWTTokenModels

__all__ = ['ICreateAccessTokenCmd']


class ICreateAccessTokenCmd:
    __slots__ = ()

    def __call__(self, payload: t.Dict[str, t.Any]) -> JWTTokenModels:
        raise NotImplementedError()
