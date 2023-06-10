import typing as t

from pydantic import BaseModel

from app.plugins.jwt_token_plugin import JWTToken
from app.plugins.jwt_token_plugin.functions.commands.impl import CreateAccessTokenCmd
from app.plugins.jwt_token_plugin.functions.commands.impl import CreateRefreshTokenCmd
from app.plugins.jwt_token_plugin.functions.commands.impl import DecodeJWTTokenCmd
from app.plugins.jwt_token_plugin.functions.commands.interfaces import ICreateAccessTokenCmd
from app.plugins.jwt_token_plugin.functions.commands.interfaces import ICreateRefreshTokenCmd
from app.plugins.jwt_token_plugin.functions.commands.interfaces import IDecodeJWTTokenCmd
from app.utils.ioc import ioc
from app.utils.plugins_manager import IPlugin
from app.utils.plugins_manager import plugins_manager

__all__ = ['JwtTokenPlugin']


class JWTTokenSettings(BaseModel):
    secret_key: str
    refresh_token_expires: int
    access_token_expires: int


class JwtTokenPlugin(IPlugin):
    __slots__ = ()

    @property
    def name(self) -> str:
        return 'jwt_token'

    async def load(self, plugins_settings: t.Mapping[str, t.Any] | None = None) -> None:
        plugins_config = JWTTokenSettings(**plugins_settings)
        token = JWTToken(key=plugins_config.secret_key)

        ioc.set(IDecodeJWTTokenCmd, DecodeJWTTokenCmd(jwt_token=token))
        ioc.set(
            ICreateAccessTokenCmd,
            CreateAccessTokenCmd(jwt_token=token, token_expires=plugins_config.access_token_expires)
        )
        ioc.set(
            ICreateRefreshTokenCmd,
            CreateRefreshTokenCmd(jwt_token=token, token_expires=plugins_config.refresh_token_expires)
        )

    async def reload(self) -> None:
        pass

    async def unload(self) -> None:
        pass


plugins_manager.add(JwtTokenPlugin())
