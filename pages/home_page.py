from typing import NoReturn

from infrastructure.di import Registry
from infrastructure.page import Page


class HomePage(Page):
    """
    Base class for page accessor.
    """
    def __init__(self, registry: Registry):
        """
        Constructor.
        :param registry: Services registry.
        """
        Page.__init__(self, registry)

    def navigate(self) -> NoReturn:
        """
        Navigate to page.
        """
        self._navigate('')
