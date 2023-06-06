from typing import Any, Dict, Mapping

import jwt

__all__ = ['Token']


class Token:
    __slots__ = (
        '_encoded',
        '_key',
        '_algorithm',
    )

    def __init__(
        self,
        payload: Dict[str, Any],
        key: str | bytes,
        headers: Dict[str, Any] | None = None,
        algorithm: str | None = "HS256",
        sort_headers: bool = True,
    ) -> None:
        self._key = key
        self._algorithm = algorithm
        self._encoded = jwt.encode(
            payload=payload, key=self._key, headers=headers,
            algorithm=algorithm, sort_headers=sort_headers,
        )

    def decode(self) -> Mapping[str, Any]:
        return jwt.decode(jwt=self._encoded, key=self._key, algorithms=self._algorithm)
