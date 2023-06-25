import typing as t

from cryptography.fernet import Fernet
from pydantic import BaseModel

from app.functions.commands.impl import CreateHistoryLoginCmd
from app.functions.commands.impl import CreateUserCmd
from app.functions.commands.interfaces import ICreateHistoryLoginCmd
from app.functions.commands.interfaces import ICreateUserCmd
from app.functions.query.impl import GetHistoryLoginQuery
from app.functions.query.impl import IdentificationUserQuery
from app.functions.query.interfaces import IGetHistoryLoginQuery
from app.functions.query.interfaces import IIdentificationUserQuery
from app.plugins.auth_plugin.impl import Fingerprint
from app.plugins.auth_plugin.impl.auth_session import AuthSessionFactory
from app.plugins.session_auth_storage_plugin.core import ISessionStorage
from app.utils.ioc import ioc
from app.utils.plugins_manager import IPlugin
from app.utils.plugins_manager import plugins_manager


class PluginsSettings(BaseModel):
    fingerprint_secret_key: str


class AuthPlugin(IPlugin):
    __slots__ = ()

    @property
    def name(self) -> str:
        return 'auth'

    async def load(self, plugins_settings: t.Mapping[str, t.Any] | None = None) -> None:
        plugin_config = PluginsSettings(**plugins_settings)
        fernet = Fernet(key=plugin_config.fingerprint_secret_key)
        fingerprint = Fingerprint(fernet=fernet)

        session_storage = ioc.get_object(object_type=ISessionStorage)()
        auth_session_factory = AuthSessionFactory(session_storage=session_storage, fingerprint=fingerprint)

        ioc.set_object(object_=fingerprint, object_type=Fingerprint)
        ioc.set_function(function_type=AuthSessionFactory, function=auth_session_factory)
        ioc.set_function(function_type=ICreateUserCmd, function=CreateUserCmd())
        ioc.set_function(function_type=IIdentificationUserQuery, function=IdentificationUserQuery())
        ioc.set_function(function_type=ICreateHistoryLoginCmd, function=CreateHistoryLoginCmd())
        ioc.set_function(function_type=IGetHistoryLoginQuery, function=GetHistoryLoginQuery())

    async def reload(self) -> None:
        pass

    async def unload(self) -> None:
        pass


plugins_manager.add(AuthPlugin())
