import os

from sys import platform

from selenium.webdriver import Chrome, ChromeOptions, Firefox, FirefoxOptions
from selenium.webdriver.remote.webdriver import WebDriver

from infrastructure.errors import TestError
from infrastructure.config import Config
from infrastructure.config_keys import WellKnownConfigKeys
from infrastructure.utils import is_uri_accessible, execute_with_retry


class WebDriverFactory:
    """
    Encapsulate instantiation of WebDriver based on configuration and environment
    """

    WEB_DRIVER_TYPE_CHROME = 'chrome'
    WEB_DRIVER_TYPE_FIREFOX = 'firefox'

    def __init__(self, config: Config):
        """
        Constructor.
        :param config: Configuration.
        """
        self._config = config

    def create(self) -> WebDriver:
        """
        Create web driver.
        """
        if self._config.get_bool(WellKnownConfigKeys.SELENIUM_REMOTE):
            return self._create_remote_driver()

        driver_type = self._config.get(WellKnownConfigKeys.SELENIUM_DRIVER)

        if driver_type == WebDriverFactory.WEB_DRIVER_TYPE_CHROME:
            return self._create_chrome_driver()

        if driver_type == WebDriverFactory.WEB_DRIVER_TYPE_FIREFOX:
            return self._create_firefox_driver()

        raise TestError('Unknown web driver type "{}"'.format(driver_type))

    def _create_remote_driver(self) -> WebDriver:
        """
        Create remote driver.
        :return: web driver.
        """
        remote_uri = self._config.get(WellKnownConfigKeys.SELENIUM_REMOTE_URI)

        if remote_uri is None:
            raise TestError('{} is missing'.format(WellKnownConfigKeys.SELENIUM_REMOTE_URI))

        driver_type = self._config.get(WellKnownConfigKeys.SELENIUM_DRIVER)

        if driver_type == WebDriverFactory.WEB_DRIVER_TYPE_CHROME:
            options = ChromeOptions()
        elif driver_type == WebDriverFactory.WEB_DRIVER_TYPE_FIREFOX:
            options = FirefoxOptions()
        else:
            raise TestError('Unknown web driver type "{}"'.format(driver_type))

        execute_with_retry(lambda: not is_uri_accessible(remote_uri),
                           timeout=self._config.get_float(WellKnownConfigKeys.WAIT_TIMEOUT))

        driver = WebDriver(command_executor=remote_uri, options=options)

        return driver

    def _create_chrome_driver(self) -> Chrome:
        """
        Create chrome driver.
        :return: web driver.
        """
        options = ChromeOptions()
        options.binary_location = os.path.join('tools',
                                               'web-drivers-chrome',
                                               self._get_platform_dependent_driver_name())

        return Chrome(options=options)

    def _create_firefox_driver(self) -> Firefox:
        """
        Create firefox driver.
        :return: web driver.
        """
        options = FirefoxOptions()
        options.binary_location = os.path.join('tools',
                                               'web-drivers-gecko',
                                               self._get_platform_dependent_driver_name())

        return Firefox(options=options)

    @staticmethod
    def _get_platform_dependent_driver_name() -> str:
        """
        Get platform dependent driver name.
        :return: platform name.
        """
        if platform in ('linux', 'linux2'):
            return 'linux'

        if platform == "win32":
            return 'win.exe'
