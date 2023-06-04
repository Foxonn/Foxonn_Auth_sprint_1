from typing import Any, Mapping, Type, TypeVar

__all__ = [
    'IOC',
    'ioc',
]

T = TypeVar("T")


class IOC:
    __slots__ = (
        '__store',
    )

    def __init__(self) -> None:
        self.__store = dict()

    def get_store(self) -> Mapping[str, Any]:
        return self.__store

    def set(self, key: Type[T], value: T) -> None:
        self.__store[key] = value

    def get(self, key: Type[T]) -> T | None:
        return self.__store[key]


ioc = IOC()
