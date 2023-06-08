from datetime import datetime
from typing import Any, Dict

import jwt

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

    @property
    def __utcnow_timestamp(self) -> int:
        return int(datetime.utcnow().strftime('%s'))

    def _calculate_token_expired(self, expire: int) -> int:
        time_expiration_token = datetime.fromtimestamp(self.__utcnow_timestamp + expire)
        return int(time_expiration_token.strftime('%s'))

    def encode(self, payload: Dict[str, Any], token_expires: int, headers: Dict[str, Any] | None = None) -> str:
        date_expired_access_token = self._calculate_token_expired(expire=token_expires)
        payload.update({'expired': date_expired_access_token})
        encode = jwt.encode(payload=payload, key=self._key, headers=headers, algorithm=self._algorithm)
        return encode

    def decode(self, jwt_encoded: str) -> Dict[str, Any]:
        return jwt.decode(jwt=jwt_encoded, key=self._key, algorithms=self._algorithm)
