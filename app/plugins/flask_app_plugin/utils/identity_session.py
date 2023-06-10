from flask import request

from app.plugins.jwt_token_plugin.functions.commands.interfaces import IDecodeJWTTokenCmd
from app.plugins.jwt_token_plugin.models import JWTTokenModels
from app.utils.ioc import ioc

__all__ = ['identity_session']


def identity_session() -> JWTTokenModels:
    decode_jwt_token_cmd = ioc.get(IDecodeJWTTokenCmd)
    authorization_token = request.headers.get('Authorization').split()[-1]
    token = decode_jwt_token_cmd(authorization_token)
    return token
