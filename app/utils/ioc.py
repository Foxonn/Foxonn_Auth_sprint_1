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
        def call() -> T:
            return object_

        self.__objects_store[object_type] = call

    def get_object(self, object_type: t.Type[T]) -> t.Callable[[None], T] | None:
        return self.__objects_store[object_type]

    def set_function(self, function_type: t.Type[T], function: T) -> None:
        self.__functions_store[function_type] = function.__call__

    def get_function(self, function_type: t.Type[T]) -> t.Callable[[None], T]:
        function = self.__functions_store[function_type]
        return function


ioc = IOC()


if __name__ == '__main__':

    class A:
        def __call__(self, msg: str) -> str:
            return msg

    ioc = IOC()
    ioc.set_function(function_type=A, function=A())
    func = ioc.get_function(function_type=A)
    print('\n'+'*'*30)
    print(*[func(123123123)], sep='\n\r')
    print('*'*30+'\n')
