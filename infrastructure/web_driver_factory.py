from selenium.webdriver import Chrome, Firefox, DesiredCapabilities
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from sys import platform

from infrastructure.errors import TestError
from infrastructure.config import Config, WellKnownConfigKeys
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
        self.__config = config

    def create(self) -> RemoteWebDriver:
        """
        Create web driver
        """

        if self.__config.get_bool(WellKnownConfigKeys.SELENIUM_REMOTE):
            return self.__create_remote_driver()

        driver_type = self.__config.get(WellKnownConfigKeys.SELENIUM_DRIVER)

        if driver_type == WebDriverFactory.WEB_DRIVER_TYPE_CHROME:
            return self.__create_chrome_driver()

        if driver_type == WebDriverFactory.WEB_DRIVER_TYPE_FIREFOX:
            return self.__create_firefox_driver()

        raise TestError('Unknown web driver type "{}"'.format(driver_type))

    def __create_remote_driver(self) -> RemoteWebDriver:
        remote_uri = self.__config.get(WellKnownConfigKeys.SELENIUM_REMOTE_URI)

        if remote_uri is None:
            raise TestError('{} is missing'.format(WellKnownConfigKeys.SELENIUM_REMOTE_URI))

        driver_type = self.__config.get(WellKnownConfigKeys.SELENIUM_DRIVER)

        if driver_type == WebDriverFactory.WEB_DRIVER_TYPE_CHROME:
            desired_capabilities = DesiredCapabilities.CHROME
        elif driver_type == WebDriverFactory.WEB_DRIVER_TYPE_FIREFOX:
            desired_capabilities = DesiredCapabilities.FIREFOX
        else:
            raise TestError('Unknown web driver type "{}"'.format(driver_type))

        execute_with_retry(lambda: not is_uri_accessible(remote_uri),
                           timeout=self.__config.get_float(WellKnownConfigKeys.WAIT_TIMEOUT))

        driver = RemoteWebDriver(command_executor=remote_uri,
                                 desired_capabilities=desired_capabilities)
        return driver

    def __create_chrome_driver(self) -> Chrome:
        executable_path = './tools/web-drivers-chrome/' \
                          + self.__get_platform_dependent_driver_name()

        driver = Chrome(executable_path=executable_path)
        return driver

    def __create_firefox_driver(self) -> Firefox:
        executable_path = './tools/web-drivers-gecko/' \
                          + self.__get_platform_dependent_driver_name()

        driver = Firefox(executable_path=executable_path)
        return driver

    def __get_platform_dependent_driver_name(self) -> str:
        if platform == 'linux' or platform == 'linux2':
            return 'linux'

        if platform == "darwin":
            return 'mac'

        if platform == "win32":
            return 'win.exe'
