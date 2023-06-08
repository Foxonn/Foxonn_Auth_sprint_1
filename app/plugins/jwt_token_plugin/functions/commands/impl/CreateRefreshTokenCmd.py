from typing import Any, Dict

from app.plugins.jwt_token_plugin import JWTToken
from app.plugins.jwt_token_plugin.functions.commands.interfaces import ICreateRefreshTokenCmd
from app.plugins.jwt_token_plugin.models import JWTTokenModels
from app.plugins.jwt_token_plugin.models.JWTTokenModels import JWTTokenPayloadsModels

__all__ = ['CreateRefreshTokenCmd']


class CreateRefreshTokenCmd(ICreateRefreshTokenCmd):
    __slots__ = (
        '_jwt_token',
        '_jwt_refresh_token_expires',
    )

    def __init__(self, jwt_token: JWTToken, jwt_refresh_token_expires: int):
        self._jwt_token = jwt_token
        self._jwt_refresh_token_expires = jwt_refresh_token_expires

    def __call__(self, payload: Dict[str, Any]) -> JWTTokenModels:
        token = JWTTokenModels(
            token=self._jwt_token.encode(payload=payload, token_expires=self._jwt_refresh_token_expires),
            payload=JWTTokenPayloadsModels(**payload),
        )
        return token
