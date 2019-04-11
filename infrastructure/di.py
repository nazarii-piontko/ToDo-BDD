from typing import TypeVar, NoReturn, Union, Type

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
        self.__registry: dict = {}

    def get(self, service_type: Type[T]) -> T:
        """
        Get service with specified type.
        :param service_type: Service type.
        :return: Service.
        """
        if service_type not in self.__registry:
            raise TestError('Type "{}" is missing in registry'.format(service_type))

        return self.__registry[service_type]

    def set(self, service: T, service_type: Union[Type[T], None] = None) -> NoReturn:
        """
        Set service with specified type
        :param service: Service
        :param service_type: Service type, if None - auto-detected
        """
        if service_type is None:
            service_type = type(service)
        self.__registry[service_type] = service

    def remove(self, service_type: Type[T]) -> NoReturn:
        """
        Remove service with specified type
        :param service_type:  Service type.
        """
        if service_type not in self.__registry:
            return
        del self.__registry[service_type]

    def clear(self) -> NoReturn:
        """
        Clear registry
        """
        self.__registry.clear()
