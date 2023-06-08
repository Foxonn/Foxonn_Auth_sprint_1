from typing import Any, Mapping

from pydantic import BaseModel

from app.plugins.jwt_token_plugin import JWTToken
from app.plugins.jwt_token_plugin.functions.commands.impl import (
    CreateAccessTokenCmdCmd,
    CreateRefreshTokenCmd,
    DecodeJWTTokenCmd,
)
from app.plugins.jwt_token_plugin.functions.commands.interfaces import (
    ICreateAccessTokenCmd,
    ICreateRefreshTokenCmd,
    IDecodeJWTTokenCmd,
)
from app.utils.ioc import ioc
from app.utils.plugins_manager import IPlugin, plugins_manager

__all__ = ['JwtTokenPlugin']


class JWTTokenSettings(BaseModel):
    jwt_secret_key: str
    jwt_refresh_token_expires: int
    jwt_access_token_expires: int


class JwtTokenPlugin(IPlugin):
    __slots__ = ()

    @property
    def name(self) -> str:
        return 'jwt_token'

    async def load(self, plugins_settings: Mapping[str, Any] | None = None) -> None:
        plugins_config = JWTTokenSettings(**plugins_settings)
        token = JWTToken(key=plugins_config.jwt_secret_key)

        ioc.set(IDecodeJWTTokenCmd, DecodeJWTTokenCmd(jwt_token=token))
        ioc.set(
            ICreateAccessTokenCmd,
            CreateAccessTokenCmdCmd(jwt_token=token, jwt_access_token_expires=plugins_config.jwt_access_token_expires)
        )
        ioc.set(
            ICreateRefreshTokenCmd,
            CreateRefreshTokenCmd(jwt_token=token, jwt_refresh_token_expires=plugins_config.jwt_refresh_token_expires)
        )

    async def reload(self) -> None:
        pass

    async def unload(self) -> None:
        pass


plugins_manager.add(JwtTokenPlugin())
