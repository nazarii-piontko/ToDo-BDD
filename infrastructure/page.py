from time import sleep
from typing import NoReturn, Union
from urllib.parse import urljoin
from os.path import join as path_join
from datetime import datetime

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from selenium.webdriver.remote.webelement import WebElement

from infrastructure.app_controller import AppController
from infrastructure.artifacts import Artifacts
from infrastructure.di import Registry
from infrastructure.errors import TestError


class Page:
    """
    Base class for page accessor.
    """
    def __init__(self, registry: Registry):
        """
        Constructor.
        :param registry: Services registry.
        """
        self._registry = registry

    def wait(self, seconds: float) -> NoReturn:
        """
        Wait specified amount of seconds.
        :param seconds: Seconds to wait, it could have seconds fractions, e.g. 0.1 -> 100 ms.
        """
        if seconds < 0:
            raise TestError('seconds cannot be less then zero: {}'.format(seconds))

        sleep(seconds)

    def create_screenshot(self) -> str:
        """
        Create current web driver page screenshot.
        :return: Screenshot path in artifacts directory.
        """
        file_name = 'screenshot-{}.png'.format(datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
        path = path_join(self._registry.get(Artifacts).get_artifacts_dir(), file_name)

        self._registry.get(RemoteWebDriver).get_screenshot_as_file(path)

        return path

    def get_element_by_css(self, css_path: str) -> Union[WebElement, None]:
        """
        Get element by CSS selector.
        :param css_path: CSS selector.
        :return: Web element.
        """
        try:
            element = self._registry.get(RemoteWebDriver).find_element_by_css_selector(css_path)
            return element
        except NoSuchElementException:
            return None

    def _navigate(self, path) -> NoReturn:
        """
        Navigate to specific page.
        :param path: Path to the page.
        """
        self._registry.get(RemoteWebDriver).get(self._get_uri(path))

    def _get_uri(self, path: str) -> str:
        """
        Get full URI for page with path.
        :param path: Path.
        """
        app = self._registry.get(AppController)
        uri = urljoin(app.get_uri(), path)
        return uri
