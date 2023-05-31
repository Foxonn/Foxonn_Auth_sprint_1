from typing import Any
from typing import Dict
from typing import List
from typing import Mapping
from typing import Type

from .IPlugin import IPlugin

__all__ = ['IPluginsManager']


class IPluginsManager:
    __slots__ = ()

    def list(self) -> Dict[Type[IPlugin], IPlugin]:
        raise NotImplementedError()

    def add(self, plugin: IPlugin) -> None:
        raise NotImplementedError()

    async def loads(self, plugins_settings: Mapping[str, Any], orders: List[str]) -> None:
        """
        Loads all plugins
        """
        raise NotImplementedError()

    async def unloads(self) -> None:
        """
        Unloads all plugins
        """
        raise NotImplementedError()

    async def reloads(self) -> None:
        """
        Reloads all plugins
        """
        raise NotImplementedError()
