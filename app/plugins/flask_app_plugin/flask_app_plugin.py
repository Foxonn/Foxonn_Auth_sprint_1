import typing as t

from flask import Flask

from app.functions.commands.interfaces import ICreateHistoryLoginCmd
from app.functions.query.interfaces import IIdentificationUserQuery
from app.plugins.flask_app_plugin.api.v1.views import init_views
from app.plugins.flask_app_plugin.events import CreateHistoryLoginEventHandler
from app.plugins.flask_app_plugin.events import LoginEvent
from app.utils.ioc import ioc
from app.utils.event_bus import event_bus
from app.utils.plugins_manager import IPlugin
from app.utils.plugins_manager import plugins_manager

__all__ = ['FlaskAppPlugin']


class FlaskAppPlugin(IPlugin):
    __slots__ = ()

    @property
    def name(self) -> str:
        return 'flask_app'

    async def load(self, plugins_settings: t.Mapping[str, t.Any] | None = None) -> None:
        app = Flask(__name__)

        event_bus.subscribe(
            event=LoginEvent,
            event_handler=CreateHistoryLoginEventHandler(
                identification_user_query=ioc.get_function(function_type=IIdentificationUserQuery),
                create_history_login_cmd=ioc.get_function(function_type=ICreateHistoryLoginCmd),
            )
        )

        ioc.set_object(object_type=Flask, object_=app)
        init_views(app=app)

    async def reload(self) -> None:
        pass

    async def unload(self) -> None:
        pass


plugins_manager.add(FlaskAppPlugin())
