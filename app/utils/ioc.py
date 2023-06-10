import typing as t

__all__ = [
    'IOC',
    'ioc',
]

T = t.TypeVar("T")


class IOC:
    __slots__ = (
        '__store',
    )

    def __init__(self) -> None:
        self.__store = dict()

    def get_store(self) -> t.Mapping[str, t.Any]:
        return self.__store

    def set(self, key: t.Type[T], value: T) -> None:
        self.__store[key] = value

    def get(self, key: t.Type[T]) -> T | None:
        return self.__store[key]


ioc = IOC()
