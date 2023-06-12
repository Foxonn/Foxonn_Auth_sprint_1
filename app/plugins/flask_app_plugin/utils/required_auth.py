import functools
import typing as t

from flask import request
from jwt import ExpiredSignatureError
from orjson import orjson

from app.models.jwt_token_models import JWTTokenModels
from app.plugins.flask_app_plugin.exceptions import FingerprintIsNotValidateError
from app.plugins.flask_app_plugin.utils.fingerprint import fingerprint_decode
from app.plugins.flask_app_plugin.utils.fingerprint import fingerprint_encode
from app.plugins.flask_app_plugin.utils.make_json_response import make_json_response
from app.plugins.jwt_token_plugin.functions.commands.interfaces import IDecodeJWTTokenCmd
from app.plugins.session_auth_storage_plugin.core import ISessionStorage
from app.utils.ioc import ioc

__all__ = ['required_auth']


def validation_token_and_fingerprint(session_storage: ISessionStorage, token: JWTTokenModels) -> bool:
    """
    Проверка идентичности fingerprint клиента и в хранилище токенов и fingerprint.
    """
    fp = fingerprint_decode(fingerprint_encode())
    fp_from_storage = fingerprint_decode(session_storage.get(token.token).payload.fingerprint[2:-1])

    if fp == fp_from_storage:
        return True
    else:
        raise FingerprintIsNotValidateError()


def required_auth(func) -> t.Callable:
    decode_jwt_token_cmd = ioc.get_function(function_type=IDecodeJWTTokenCmd)
    session_storage = ioc.get_object(object_type=ISessionStorage)()

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        authorization_token = request.headers.get('Authorization').split()[-1]
        try:
            token_model = decode_jwt_token_cmd(token=authorization_token)
            validation_token_and_fingerprint(session_storage=session_storage, token=token_model)
        except ExpiredSignatureError as err:
            return make_json_response(response=orjson.dumps({'error': f'Access token. {err}'}), status=401)
        except FingerprintIsNotValidateError as err:
            return make_json_response(response=orjson.dumps({'error': f'Invalidate token. {err}'}), status=403)
        return await func(*args, **kwargs)

    return wrapper
