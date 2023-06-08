from app.plugins.jwt_token_plugin import JWTToken
from app.plugins.jwt_token_plugin.functions.commands.interfaces import IDecodeJWTTokenCmd
from app.plugins.jwt_token_plugin.models import JWTTokenModels, JWTTokenPayloadsModels

__all__ = ['DecodeJWTTokenCmd']


class DecodeJWTTokenCmd(IDecodeJWTTokenCmd):
    __slots__ = (
        '_jwt_token',
    )

    def __init__(self, jwt_token: JWTToken) -> None:
        self._jwt_token = jwt_token

    def __call__(self, token: str) -> JWTTokenModels:
        decode = self._jwt_token.decode(token)
        return JWTTokenModels(token=token, payload=JWTTokenPayloadsModels(**decode))
