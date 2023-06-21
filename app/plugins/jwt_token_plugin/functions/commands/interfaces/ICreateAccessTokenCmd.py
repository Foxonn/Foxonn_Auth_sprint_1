import typing as t

from app.models.jwt_token_models import JWTAccessTokenModels

__all__ = ['ICreateAccessTokenCmd']


class ICreateAccessTokenCmd:
    __slots__ = ()

    def __call__(self, payload: t.Dict[str, t.Any]) -> JWTAccessTokenModels:
        raise NotImplementedError()
