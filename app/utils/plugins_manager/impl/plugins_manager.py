import asyncio
import logging
from collections import UserDict
from typing import Any
from typing import ItemsView
from typing import List
from typing import Mapping

from ..interfaces import IPlugin
from ..interfaces import IPluginsManager

__all__ = [
    'PluginsManager',
    'plugins_manager',
]


class PluginsStore(UserDict[str, IPlugin]):

    def __setitem__(self, key: str, item: IPlugin) -> None:
        super().__setitem__(key, item)

    def __getitem__(self, item: str) -> IPlugin:
        return super().__getitem__(item)


class PluginsManager(IPluginsManager):
    __slots__ = (
        '__plugins_store',
    )

    def __init__(self) -> None:
        self.__plugins_store = PluginsStore()

    def list(self) -> ItemsView[str, IPlugin]:
        return self.__plugins_store.items()

    def add(self, plugin: IPlugin) -> None:
        self.__plugins_store[plugin.name] = plugin

    def get(self, plugin_name: str) -> IPlugin:
        return self.__plugins_store[plugin_name]

    async def loads(self, orders: List[str], plugins_settings: Mapping[str, Any] = {}) -> None:
        set_orders = set(orders)
        plugins_names = self.__plugins_store.keys()

        if diff := set_orders.difference(plugins_names):
            logging.warning(f'Plugin: {diff}, not found in list plugin loads.')

        list_name_plugins_load = set_orders.intersection(plugins_names)

        for plugin_name in list(list_name_plugins_load)[::-1]:
            plugin = self.__plugins_store[plugin_name]
            if settings := plugins_settings.get(plugin.name, None):
                asyncio.create_task(plugin.load(settings))
            else:
                asyncio.create_task(plugin.load())
            logging.debug(f'Plugin: `{plugin.name}` started to load.')

    async def unloads(self) -> None:
        await asyncio.gather(*[plugin.unload() for plugin in self.__plugins_store.values()])

    async def reloads(self) -> None:
        await asyncio.gather(*[plugin.reload() for plugin in self.__plugins_store.values()])


plugins_manager = PluginsManager()
