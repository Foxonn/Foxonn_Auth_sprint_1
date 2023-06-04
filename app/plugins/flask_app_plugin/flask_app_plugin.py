from typing import Any, Mapping

from flask import Flask
from flask_jwt_extended import JWTManager
from pydantic import BaseModel

from app.plugins.flask_app_plugin.api.v1.views import init_views
from app.utils.ioc import ioc
from app.utils.plugins_manager import IPlugin, plugins_manager

__all__ = ['FlaskAppPlugin']


class PluginsSettings(BaseModel):
    jwt_secret_key: str
    jwt_access_token_expires: int
    jwt_refresh_token_expires: int


class FlaskAppPlugin(IPlugin):
    __slots__ = ()

    @property
    def name(self) -> str:
        return 'flask_app'

    async def load(self, plugins_settings: Mapping[str, Any] | None = None) -> None:
        config = PluginsSettings(**plugins_settings)
        app = Flask(__name__)

        app.config["JWT_SECRET_KEY"] = config.jwt_secret_key
        app.config["JWT_ACCESS_TOKEN_EXPIRES"] = config.jwt_access_token_expires
        app.config["JWT_REFRESH_TOKEN_EXPIRES"] = config.jwt_refresh_token_expires

        jwt = JWTManager(app)

        ioc.set(Flask, app)
        ioc.set(JWTManager, jwt)

        init_views(app=app)

    async def reload(self) -> None:
        pass

    async def unload(self) -> None:
        pass


plugins_manager.add(FlaskAppPlugin())
