from infrastucture.app_controller import AppController
from infrastucture.web_driver_factory import WebDriverFactory
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from urllib.parse import urljoin


class TestingContext:
    """
    Encapsulate lifecycle and access to application under test
    """
    def __init__(self):
        self.__web_driver = None
        self.__app_controller = AppController()

    def start(self) -> None:
        self.__app_controller.start()
        self.__web_driver = WebDriverFactory().create()

    def stop(self) -> None:
        self.__app_controller.stop()
        self.__web_driver.quit()

    def get_web_driver(self) -> RemoteWebDriver:
        return self.__web_driver

    def get_uri(self, path: str) -> str:
        return urljoin(self.__app_controller.get_base_uri(), path)
