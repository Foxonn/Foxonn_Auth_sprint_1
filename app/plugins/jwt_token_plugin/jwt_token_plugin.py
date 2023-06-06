from typing import Any, Mapping

from app.utils.plugins_manager import IPlugin

__all__ = ['JwtTokenPlugin']


class JwtTokenPlugin(IPlugin):
    __slots__ = ()

    @property
    def name(self) -> str:
        return 'jwt_token'

    async def load(self, plugins_settings: Mapping[str, Any] | None = None) -> None:
        ...

    async def reload(self) -> None:
        pass

    async def unload(self) -> None:
        pass
