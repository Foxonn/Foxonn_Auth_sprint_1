import typing as t

from cryptography.fernet import Fernet
from flask import Request
from flask import request
from orjson import orjson

from app.utils.ioc import ioc

__all__ = [
    'fingerprint_encode',
    'fingerprint_decode',
]


def fingerprint_encode() -> bytes:
    fernet = ioc.get(Fernet)
    return _fingerprint_encode(fernet=fernet, request=request)


def fingerprint_decode(fingerprint: bytes) -> t.Dict[str, t.Any]:
    fernet = ioc.get(Fernet)
    return _fingerprint_decode(fernet=fernet, fingerprint=fingerprint)


def _fingerprint_encode(request: Request, fernet: Fernet) -> bytes:
    fingerprint_payload = orjson.dumps(
        {'device': request.headers['User-Agent'],
         'remote_addr': request.remote_addr},
    )
    fingerprint = fernet.encrypt(data=fingerprint_payload)
    return fingerprint


def _fingerprint_decode(fernet: Fernet, fingerprint: bytes) -> t.Dict[str, t.Any]:
    fingerprint = fernet.decrypt(fingerprint)
    raw_data = orjson.loads(fingerprint)
    return raw_data
