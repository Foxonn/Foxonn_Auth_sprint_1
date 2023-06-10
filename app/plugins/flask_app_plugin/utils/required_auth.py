import functools
import typing as t

from flask import request
from jwt import ExpiredSignatureError
from orjson import orjson

from app.plugins.flask_app_plugin.utils.make_json_response import make_json_response
from app.plugins.jwt_token_plugin.functions.commands.interfaces import IDecodeJWTTokenCmd
from app.utils.ioc import ioc

__all__ = ['required_auth']


def required_auth(func) -> t.Callable:
    decode_jwt_token_cmd = ioc.get(IDecodeJWTTokenCmd)

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        authorization_token = request.headers.get('Authorization').split()[-1]
        try:
            decode_jwt_token_cmd(authorization_token)
        except ExpiredSignatureError as err:
            return make_json_response(response=orjson.dumps({'error': f'Access token. {err}'}), status=401)
        return await func(*args, **kwargs)

    return wrapper
