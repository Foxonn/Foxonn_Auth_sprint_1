from flask import request
from jwt import ExpiredSignatureError

from app.models.jwt_token_models import JWTTokenModels
from app.plugins.flask_app_plugin.exceptions import BearerTokenNotFoundError
from app.plugins.flask_app_plugin.exceptions import TokenExpiredError
from app.plugins.jwt_token_plugin.functions.commands.interfaces import IDecodeJWTTokenCmd
from app.utils.ioc import ioc

__all__ = ['get_token_session']


def get_token_session() -> JWTTokenModels:
    decode_jwt_token_cmd = ioc.get_function(function_type=IDecodeJWTTokenCmd)
    authorization_header = request.headers.get('Authorization')

    if not authorization_header:
        raise BearerTokenNotFoundError()

    authorization_token = authorization_header.split()[-1]

    try:
        token = decode_jwt_token_cmd(authorization_token)
    except ExpiredSignatureError:
        raise TokenExpiredError()
    return token
