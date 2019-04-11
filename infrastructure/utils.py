from typing import Any, NoReturn, Callable
from infrastructure.di import Registry
from time import sleep, monotonic_ns


def get_registry(context: Any) -> Registry:
    """
    Get services registry from behave context.
    :param context: Behave context.
    :return: Services registry.
    """
    return context.registry


def set_registry(context: Any, registry: Registry) -> NoReturn:
    """
    Set services registry to behave context.
    :param context: Behave context.
    :param registry: Services registry.
    """
    context.registry = registry


def is_uri_accessible(uri: str) -> bool:
    """
    Check if specified URI is accessible.
    :param uri: URI for probe.
    :return: True of uri is accessible, otherwise False.
    """
    import requests
    try:
        requests.head(uri)
        return True
    except requests.ConnectionError:
        return False


def execute_with_retry(action: Callable[[], bool],
                       sleep_time: float = 0.1,
                       timeout: float = 0.1) -> NoReturn:
    """
    Execute some action with retry with sleep and timeout.
    It is necessary for different waiting operations.
    :param action: Action.
    :param sleep_time: Sleep time in seconds.
    :param timeout: Timeout in seconds.
    """
    timeout_ns = int(timeout * 1e9)
    start_time = monotonic_ns()

    while True:
        retry = action()

        if not retry:
            break

        if monotonic_ns() - start_time >= timeout_ns:
            raise TimeoutError

        sleep(sleep_time)

        if monotonic_ns() - start_time >= timeout_ns:
            raise TimeoutError
