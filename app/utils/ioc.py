import typing as t

__all__ = [
    'IOC',
    'ioc',
]

T = t.TypeVar("T")


class IOC:
    __slots__ = (
        '__objects_store',
        '__functions_store',
    )

    def __init__(self) -> None:
        self.__objects_store: t.Dict[t.Type, t.Any] = dict()
        self.__functions_store: t.Dict[t.Type, t.Callable] = dict()

    def set_object(self, object_type: t.Type[T], object_: T) -> None:
        def _() -> T:
            return object_

        self.__objects_store[object_type] = _

    def get_object(self, object_type: t.Type[T]) -> t.Callable[[None], T]:
        def _() -> t.Callable:
            return self.__objects_store[object_type]()
        return _

    def set_function(self, function_type: t.Type[T], function: T) -> None:
        self.__functions_store[function_type] = function.__call__

    def get_function(self, function_type: t.Type[T]) -> T:
        def _(*args, **kwargs) -> t.Callable:
            return self.__functions_store[function_type](*args, **kwargs)
        return _


ioc = IOC()
