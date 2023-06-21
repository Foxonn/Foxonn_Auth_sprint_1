import datetime
import typing as t

import jwt

from app.models.jwt_token_models import JWTTokenModels

__all__ = ['JWTToken']


class JWTToken:
    __slots__ = (
        '_key',
        '_algorithm',
        '_sort_headers',
        '_headers',
    )

    def __init__(
        self,
        key: str | bytes,
        algorithm: str | None = "HS256",
    ) -> None:
        self._key = key
        self._algorithm = algorithm

    def encode(
        self,
        payload: t.Dict[str, t.Any],
        token_expires: int,
        headers: t.Dict[str, t.Any] | None = None,
    ) -> JWTTokenModels:
        date_expired_access_token = datetime.datetime.utcnow() + datetime.timedelta(seconds=token_expires)
        payload.update({'exp': date_expired_access_token})
        encode = jwt.encode(payload=payload, key=self._key, headers=headers, algorithm=self._algorithm)
        return JWTTokenModels(token=encode, payload=payload)

    def decode(self, jwt_encoded: str) -> t.Dict[str, t.Any]:
        return jwt.decode(jwt=jwt_encoded, key=self._key, algorithms=self._algorithm)
