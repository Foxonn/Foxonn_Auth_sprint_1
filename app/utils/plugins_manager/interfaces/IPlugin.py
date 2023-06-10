import typing as t

__all__ = ['IPlugin']


class IPlugin:
    __slots__ = ()

    @property
    def name(self) -> str:
        raise NotImplementedError()

    async def load(self, plugins_settings: t.Mapping[str, t.Any] | None = None) -> None:
        raise NotImplementedError()

    async def reload(self) -> None:
        raise NotImplementedError()

    async def unload(self) -> None:
        raise NotImplementedError()
