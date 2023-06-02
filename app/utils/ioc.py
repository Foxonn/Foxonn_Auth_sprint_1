import logging
import typing
from typing import Any
from typing import Type
from typing import TypeVar
from typing import Mapping

from tenacity import _utils
from tenacity import retry
from tenacity import retry_if_exception_type
from tenacity import stop_after_attempt
from tenacity import wait_fixed

__all__ = [
    'IOC',
    'ioc',
]

T = TypeVar("T")

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger('ioc')


def before_log(logger: "logging.Logger", log_level: int, data: Any) -> typing.Callable[["RetryCallState"], None]:
    """Before call strategy that logs to some logger the attempt."""

    def log_it(retry_state: "RetryCallState") -> None:
        if retry_state.fn is None:
            # NOTE(sileht): can't really happen, but we must please mypy
            fn_name = "<unknown>"
        else:
            fn_name = _utils.get_callback_name(retry_state.fn)
        logger.log(
            log_level,
            (
                f"Starting call to '{fn_name}', "
                f"this is the {_utils.to_ordinal(retry_state.attempt_number)} time calling it."
                f"Data: {data}"
            ),
        )

    return log_it


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
        @retry(
            retry=retry_if_exception_type(KeyError),
            wait=wait_fixed(1),
            stop=stop_after_attempt(30),
            before=before_log(logger, logging.DEBUG, {'key': key})
        )
        def _() -> T | None:
            return self.__store[key]

        return _()


ioc = IOC()
