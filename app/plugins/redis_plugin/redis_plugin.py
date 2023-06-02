from typing import Any
from typing import Mapping

from aioredis import Redis
from pydantic import BaseModel

from app.utils.ioc import ioc
from app.utils.plugins_manager import IPlugin

__all__ = ['RedisPlugin']


class PluginsSettings(BaseModel):
    host: str
    port: int
    db: int


class RedisPlugin(IPlugin):
    @property
    def name(self) -> str:
        return 'redis'

    async def load(self, plugins_settings: Mapping[str, Any] | None = None) -> None:
        settings = PluginsSettings(**plugins_settings)
        redis_db = Redis(host=settings.host, port=settings.port, db=settings.db)
        ioc.set(Redis, redis_db)

    async def reload(self) -> None:
        pass

    async def unload(self) -> None:
        pass
