import functools
import typing as t

from jwt import ExpiredSignatureError
from orjson import orjson

from app.models.jwt_token_models import JWTTokenModels
from app.plugins.flask_app_plugin.exceptions import FingerprintIsNotValidateError
from app.plugins.flask_app_plugin.exceptions import TokenNotActiveError
from app.plugins.flask_app_plugin.utils.fingerprint import fingerprint_decode
from app.plugins.flask_app_plugin.utils.fingerprint import fingerprint_encode
from app.plugins.flask_app_plugin.utils.get_token_session import get_token_session
from app.plugins.flask_app_plugin.utils.make_json_response import make_json_response
from app.plugins.jwt_token_plugin.functions.commands.interfaces import IDecodeJWTTokenCmd
from app.plugins.session_auth_storage_plugin.core import ISessionStorage
from app.utils.ioc import ioc

__all__ = [
    'required_auth',
    'validation_fingerprint_decorator',
    'validation_token_and_fingerprint',
]

decode_jwt_token_cmd = ioc.get_function(function_type=IDecodeJWTTokenCmd)
get_session_storage = ioc.get_object(object_type=ISessionStorage)


def validation_token_and_fingerprint(session_storage: ISessionStorage, token: JWTTokenModels) -> bool:
    """
    Проверка идентичности fingerprint клиента и в хранилище токенов и fingerprint.

    fp_from_storage = fingerprint_decode(session_storage.get(token.token).payload.fingerprint[2:-1])
    байты обернуты в строку, убираем кавычки по краям и читаем как байты
    """
    fp = fingerprint_decode(fingerprint_encode())
    try:
        fp_from_storage = fingerprint_decode(session_storage.get(token.token).payload.fingerprint[2:-1])
    except KeyError:
        raise TokenNotActiveError()

    if fp == fp_from_storage:
        return True
    else:
        raise FingerprintIsNotValidateError()


def validate_authorization_token(session_storage: ISessionStorage) -> None:
    """
    Проверка токена авторизации на существование в хранилище сессий.
    """
    token = get_token_session()

    if not session_storage.is_active_token(token=token.token):
        raise TokenNotActiveError()


def validation_fingerprint_decorator(func) -> t.Callable:
    session_storage = get_session_storage()

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            token = get_token_session()
            token_model = decode_jwt_token_cmd(token=token.token)
            validation_token_and_fingerprint(session_storage=session_storage, token=token_model)
        except ExpiredSignatureError as err:
            return make_json_response(response=orjson.dumps({'error': str(err)}), status=401)
        except FingerprintIsNotValidateError as err:
            return make_json_response(response=orjson.dumps({'error': f'Invalidate token. {err}'}), status=403)
        return await func(*args, **kwargs)
    return wrapper


def required_auth_decorator(func) -> t.Callable:
    session_storage = get_session_storage()

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            token = get_token_session()
            validate_authorization_token(session_storage=session_storage)
            validation_token_and_fingerprint(session_storage=session_storage, token=token)

        except (
            TokenNotActiveError,
            FingerprintIsNotValidateError,
            ExpiredSignatureError,
        ) as err:
            return make_json_response(response=orjson.dumps({'error': str(err)}), status=401)
        return await func(*args, **kwargs)

    return wrapper
