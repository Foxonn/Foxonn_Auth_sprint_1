from typing import Any, Mapping

from app.functions.commands.impl import CreateHistoryLogin, CreateUser
from app.functions.commands.interfaces import ICreateHistoryLogin, ICreateUser
from app.functions.query.impl import GetHistoryLogin, IdentificationUser
from app.functions.query.interfaces import IGetHistoryLogin, IIdentificationUser
from app.utils.ioc import ioc
from app.utils.plugins_manager import IPlugin, plugins_manager


class AppPlugin(IPlugin):
    __slots__ = ()

    @property
    def name(self) -> str:
        return 'app'

    async def load(self, plugins_settings: Mapping[str, Any] | None = None) -> None:
        ioc.set(ICreateUser, CreateUser())
        ioc.set(IIdentificationUser, IdentificationUser())
        ioc.set(ICreateHistoryLogin, CreateHistoryLogin())
        ioc.set(IGetHistoryLogin, GetHistoryLogin())

    async def reload(self) -> None:
        pass

    async def unload(self) -> None:
        pass


plugins_manager.add(AppPlugin())
