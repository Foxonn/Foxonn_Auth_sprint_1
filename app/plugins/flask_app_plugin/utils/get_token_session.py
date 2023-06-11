from flask import request

from app.models.jwt_token_models import JWTTokenModels
from app.plugins.jwt_token_plugin.functions.commands.interfaces import IDecodeJWTTokenCmd
from app.utils.ioc import ioc

__all__ = ['get_token_session']


def get_token_session() -> JWTTokenModels:
    decode_jwt_token_cmd = ioc.get_function(function_type=IDecodeJWTTokenCmd)
    authorization_token = request.headers.get('Authorization').split()[-1]
    token = decode_jwt_token_cmd(authorization_token)
    return token
