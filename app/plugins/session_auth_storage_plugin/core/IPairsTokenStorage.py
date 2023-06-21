import typing as t

from app.models.jwt_token_models import JWTAccessTokenModels
from app.models.jwt_token_models import JWTRefreshTokenModels

__all__ = [
    'IPairsTokenStorage',
]


class IPairsTokenStorage:
    __slots__ = ()

    def set(self, access_token: JWTAccessTokenModels, refresh_token: JWTRefreshTokenModels) -> None:
        raise NotImplementedError()

    def revoke_token(self, token: str) -> None:
        raise NotImplementedError()

    def get(self, token: str) -> t.Tuple[str, str]:
        raise NotImplementedError()
