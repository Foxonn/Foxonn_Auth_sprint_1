from app.plugins.pony_db_plugin.models import User

__all__ = ['IIdentificationUser']


class IIdentificationUser:
    __slots__ = ()

    async def __call__(self, login: str, password: str) -> User:
        raise NotImplementedError()
