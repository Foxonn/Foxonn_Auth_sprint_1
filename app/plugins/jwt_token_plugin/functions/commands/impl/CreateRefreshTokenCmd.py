import typing as t

from app.models.jwt_token_models import JWTTokenModels
from app.plugins.jwt_token_plugin import JWTToken
from app.plugins.jwt_token_plugin.functions.commands.interfaces import ICreateRefreshTokenCmd

__all__ = ['CreateRefreshTokenCmd']


class CreateRefreshTokenCmd(ICreateRefreshTokenCmd):
    __slots__ = (
        '_jwt_token',
        '_token_expires',
    )

    def __init__(self, jwt_token: JWTToken, token_expires: int):
        self._jwt_token = jwt_token
        self._token_expires = token_expires

    def __call__(self, payload: t.Dict[str, t.Any]) -> JWTTokenModels:
        payload.update({'exp': self._token_expires})
        return self._jwt_token.encode(payload=payload, token_expires=self._token_expires)
