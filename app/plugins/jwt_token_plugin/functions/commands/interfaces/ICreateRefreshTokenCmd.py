from typing import Any, Dict

from app.plugins.jwt_token_plugin.models import JWTTokenModels

__all__ = ['ICreateRefreshTokenCmd']


class ICreateRefreshTokenCmd:
    __slots__ = ()

    def __call__(self, payload: Dict[str, Any]) -> JWTTokenModels:
        raise NotImplementedError()
