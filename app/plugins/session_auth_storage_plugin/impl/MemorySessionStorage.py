import orjson

from app.models.jwt_token_models import JWTTokenModels
from app.plugins.session_auth_storage_plugin.core import ISessionStorage

__all__ = ['MemorySessionStorage']


class MemorySessionStorage(ISessionStorage):
    __slots__ = (
        '_store'
    )

    def __init__(self) -> None:
        self._store = dict()

    def set(self, jwt_token: JWTTokenModels) -> None:
        self._store[jwt_token.token] = orjson.dumps(jwt_token.dict())

    def get(self, token: str) -> JWTTokenModels:
        raw_data = orjson.loads(self._store[token])
        return JWTTokenModels(**raw_data)
