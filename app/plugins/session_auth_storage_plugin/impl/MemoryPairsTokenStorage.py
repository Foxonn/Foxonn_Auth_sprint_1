import typing as t

from app.models.jwt_token_models import JWTAccessTokenModels
from app.models.jwt_token_models import JWTRefreshTokenModels
from app.plugins.session_auth_storage_plugin.core import IPairsTokenStorage

__all__ = ['MemoryPairsTokenStorage']


class MemoryPairsTokenStorage(IPairsTokenStorage):
    __slots__ = (
        '_store'
    )

    def __init__(self) -> None:
        self._store = dict()

    def set(self, access_token: JWTAccessTokenModels, refresh_token: JWTRefreshTokenModels) -> None:
        self._store[access_token.token] = refresh_token.token

    def revoke_token(self, token: str) -> None:
        self._store.pop(token)

    def get(self, token: str) -> t.Tuple[str, str]:
        refresh = self._store[token]
        return token, refresh

