import typing as t

from app.functions.commands.impl import CreateHistoryLoginCmd
from app.functions.commands.impl import CreateUserCmd
from app.functions.commands.interfaces import ICreateHistoryLoginCmd
from app.functions.commands.interfaces import ICreateUserCmd
from app.functions.query.impl import GetHistoryLoginQuery
from app.functions.query.impl import IdentificationUserQuery
from app.functions.query.interfaces import IGetHistoryLoginQuery
from app.functions.query.interfaces import IIdentificationUserQuery
from app.utils.ioc import ioc
from app.utils.plugins_manager import IPlugin
from app.utils.plugins_manager import plugins_manager


class AppPlugin(IPlugin):
    __slots__ = ()

    @property
    def name(self) -> str:
        return 'app'

    async def load(self, plugins_settings: t.Mapping[str, t.Any] | None = None) -> None:
        ioc.set_function(function_type=ICreateUserCmd, function=CreateUserCmd())
        ioc.set_function(function_type=IIdentificationUserQuery, function=IdentificationUserQuery())
        ioc.set_function(function_type=ICreateHistoryLoginCmd, function=CreateHistoryLoginCmd())
        ioc.set_function(function_type=IGetHistoryLoginQuery, function=GetHistoryLoginQuery())

    async def reload(self) -> None:
        pass

    async def unload(self) -> None:
        pass


plugins_manager.add(AppPlugin())
