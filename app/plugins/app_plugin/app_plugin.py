import typing as t

from app.functions.commands.impl import CreateHistoryLogin
from app.functions.commands.impl import CreateUser
from app.functions.commands.interfaces import ICreateHistoryLogin
from app.functions.commands.interfaces import ICreateUser
from app.functions.query.impl import GetHistoryLogin
from app.functions.query.impl import IdentificationUser
from app.functions.query.interfaces import IGetHistoryLogin
from app.functions.query.interfaces import IIdentificationUser
from app.utils.ioc import ioc
from app.utils.plugins_manager import IPlugin
from app.utils.plugins_manager import plugins_manager


class AppPlugin(IPlugin):
    __slots__ = ()

    @property
    def name(self) -> str:
        return 'app'

    async def load(self, plugins_settings: t.Mapping[str, t.Any] | None = None) -> None:
        ioc.set(ICreateUser, CreateUser())
        ioc.set(IIdentificationUser, IdentificationUser())
        ioc.set(ICreateHistoryLogin, CreateHistoryLogin())
        ioc.set(IGetHistoryLogin, GetHistoryLogin())

    async def reload(self) -> None:
        pass

    async def unload(self) -> None:
        pass


plugins_manager.add(AppPlugin())
