from typing import NoReturn

from infrastructure.di import Registry
from pages.page import Page


class HomePage(Page):
    """
    Base class for page accessor
    """
    def __init__(self, registry: Registry):
        Page.__init__(self, registry)

    def navigate(self) -> NoReturn:
        self._navigate('')
