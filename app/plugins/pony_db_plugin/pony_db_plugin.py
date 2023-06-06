from typing import Any, Mapping

from pony.orm import Database, set_sql_debug
from pydantic import BaseModel

from app.functions.commands.interfaces import ICreateUser
from app.plugins.pony_db_plugin.models import db
from app.utils.ioc import ioc
from app.utils.plugins_manager import IPlugin
from app.utils.plugins_manager.impl import plugins_manager

__all__ = ['PonyDBPlugin']


class PluginsSettingsModel(BaseModel):
    user: str
    password: str
    port: str
    host: str
    database: str
    debug: bool


class PonyDBPlugin(IPlugin):
    __slots__ = ()

    def __init__(self) -> None:
        pass

    @property
    def name(self) -> str:
        return 'pony_db'

    async def load(self, plugins_settings: Mapping[str, Any] | None = None) -> None:
        config = PluginsSettingsModel(**plugins_settings)
        set_sql_debug(debug=config.debug)
        db.bind(
            provider='postgres', user=config.user, password=config.password,
            port=config.port, host=config.host, database=config.database,
        )
        db.generate_mapping(create_tables=True)

    async def reload(self) -> None:
        pass

    async def unload(self) -> None:
        pass


plugins_manager.add(PonyDBPlugin())
