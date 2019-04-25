from typing import TypeVar, NoReturn, Union, Type, Any

from infrastructure.errors import TestError

T = TypeVar('T')


class Registry:
    """
    Services registry
    """
    def __init__(self):
        """
        Constructor.
        """
        self._registry: dict = {}

    def get(self, service_type: Type[T]) -> T:
        """
        Get service with specified type.
        :param service_type: Service type.
        :return: Service.
        """
        if service_type not in self._registry:
            raise TestError('Type "{}" is missing in registry'.format(service_type))

        return self._registry[service_type]

    def set(self, service: T, service_type: Union[Type[T], None] = None) -> NoReturn:
        """
        Set service with specified type
        :param service: Service
        :param service_type: Service type, if None - auto-detected
        """
        if service_type is None:
            service_type = type(service)

        if service_type in self._registry:
            raise TestError('Service with type {} is already registered'.format(service_type))

        self._registry[service_type] = service

    def remove(self, service_type: Type[T]) -> NoReturn:
        """
        Remove service with specified type
        :param service_type:  Service type.
        """
        if service_type not in self._registry:
            return

        del self._registry[service_type]

    def clear(self) -> NoReturn:
        """
        Clear registry
        """
        self._registry.clear()

    def __getitem__(self, service_type: Type[T]) -> T:
        return self.get(service_type)


def reg(context: Any) -> Registry:
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
