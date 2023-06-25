from flask import request
from jwt import ExpiredSignatureError

from app.plugins.auth_plugin.impl.auth_session import AuthSession
from app.plugins.auth_plugin.impl.auth_session import AuthSessionFactory
from app.plugins.auth_plugin.exceptions import BearerTokenNotFoundError
from app.plugins.auth_plugin.exceptions import TokenExpiredError
from app.plugins.jwt_token_plugin.functions.commands.interfaces import IDecodeJWTTokenCmd
from app.utils.ioc import ioc

__all__ = ['get_auth_session']

auth_session_factory = ioc.get_function(function_type=AuthSessionFactory)


async def get_auth_session() -> AuthSession:
    decode_jwt_token_cmd = ioc.get_function(function_type=IDecodeJWTTokenCmd)
    authorization_header = request.headers.get('Authorization')

    if not authorization_header:
        raise BearerTokenNotFoundError()

    authorization_token = authorization_header.split()[-1]

    try:
        token = decode_jwt_token_cmd(token=authorization_token)
        return await auth_session_factory(jwt_token=token)
    except ExpiredSignatureError:
        raise TokenExpiredError()
