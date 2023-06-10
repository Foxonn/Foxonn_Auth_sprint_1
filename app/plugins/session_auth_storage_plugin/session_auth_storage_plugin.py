import typing as t

from pydantic import BaseModel

from app.plugins.session_auth_storage_plugin.core import ISessionStorage
from app.plugins.session_auth_storage_plugin.impl import MemorySessionStorage
from app.utils.ioc import ioc
from app.utils.plugins_manager import IPlugin

__all__ = ['SessionAuthStoragePlugin']


class PluginSettings(BaseModel):
    type_storage: str


class SessionAuthStoragePlugin(IPlugin):
    __slots__ = ()

    @property
    def name(self) -> str:
        return 'session_storage'

    async def load(self, plugins_settings: t.Mapping[str, t.Any] | None = None) -> None:
        config_plugin = PluginSettings(**plugins_settings)
        ioc.set(ISessionStorage,  MemorySessionStorage())

    async def reload(self) -> None:
        pass

    async def unload(self) -> None:
        pass
