import typing as t

from aioredis import Redis
from pydantic import BaseModel

from app.utils.ioc import ioc
from app.utils.plugins_manager import IPlugin
from app.utils.plugins_manager import plugins_manager

__all__ = ['RedisPlugin']


class PluginsSettings(BaseModel):
    host: str
    port: int
    db: int


class RedisPlugin(IPlugin):
    @property
    def name(self) -> str:
        return 'redis'

    async def load(self, plugins_settings: t.Mapping[str, t.Any] | None = None) -> None:
        settings = PluginsSettings(**plugins_settings)
        redis_db = Redis(host=settings.host, port=settings.port, db=settings.db)
        ioc.set(Redis, redis_db)

    async def reload(self) -> None:
        pass

    async def unload(self) -> None:
        pass


plugins_manager.add(RedisPlugin())
