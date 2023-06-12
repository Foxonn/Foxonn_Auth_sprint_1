import typing as t

from cryptography.fernet import Fernet
from flask import Flask
from pydantic import BaseModel

from app.functions.commands.interfaces import ICreateHistoryLoginCmd
from app.functions.query.interfaces import IIdentificationUserQuery
from app.plugins.flask_app_plugin.api.v1.views import init_views
from app.plugins.flask_app_plugin.events import LoginEvent
from app.plugins.flask_app_plugin.events import CreateHistoryLoginEventHandler
from app.utils.ioc import ioc
from app.utils.message_bus import message_bus
from app.utils.plugins_manager import IPlugin
from app.utils.plugins_manager import plugins_manager

__all__ = ['FlaskAppPlugin']


class PluginsSettings(BaseModel):
    fingerprint_secret_key: str


class FlaskAppPlugin(IPlugin):
    __slots__ = ()

    @property
    def name(self) -> str:
        return 'flask_app'

    async def load(self, plugins_settings: t.Mapping[str, t.Any] | None = None) -> None:
        plugin_config = PluginsSettings(**plugins_settings)
        app = Flask(__name__)
        fernet = Fernet(key=plugin_config.fingerprint_secret_key)

        message_bus.subscribe(
            event=LoginEvent,
            event_handler=CreateHistoryLoginEventHandler(
                identification_user_query=ioc.get_function(function_type=IIdentificationUserQuery),
                create_history_login_cmd=ioc.get_function(function_type=ICreateHistoryLoginCmd),
            )
        )

        ioc.set_object(object_type=Flask, object_=app)
        ioc.set_object(object_type=Fernet, object_=fernet)
        init_views(app=app)

    async def reload(self) -> None:
        pass

    async def unload(self) -> None:
        pass


plugins_manager.add(FlaskAppPlugin())
