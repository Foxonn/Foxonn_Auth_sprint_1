import typing as t

from cryptography.fernet import Fernet
from flask import request
from orjson import orjson

__all__ = ['Fingerprint']


class Fingerprint:
    __slots__ = (
        '_fernet',
    )

    def __init__(self, fernet: Fernet) -> None:
        self._fernet = fernet

    def fingerprint_encode(self) -> bytes:
        fingerprint_payload = orjson.dumps(
            {'device': request.headers['User-Agent'],
             'remote_addr': request.remote_addr},
        )
        fingerprint = self._fernet.encrypt(data=fingerprint_payload)
        return fingerprint

    def fingerprint_decode(self, fingerprint: bytes) -> t.Dict[str, t.Any]:
        fingerprint = self._fernet.decrypt(fingerprint)
        raw_data = orjson.loads(fingerprint)
        return raw_data
