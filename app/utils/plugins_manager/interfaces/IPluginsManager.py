import typing as t

from .IPlugin import IPlugin

__all__ = ['IPluginsManager']


class IPluginsManager:
    __slots__ = ()

    def list(self) -> t.Dict[t.Type[IPlugin], IPlugin]:
        raise NotImplementedError()

    def add(self, plugin: IPlugin) -> None:
        raise NotImplementedError()

    async def loads(self, plugins_settings: t.Mapping[str, t.Any], orders: t.List[str]) -> None:
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
