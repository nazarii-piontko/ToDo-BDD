from selenium.webdriver.remote.webdriver import WebDriver


class Session:
    """
    Browser session
    """
    def __init__(self, name: str, web_driver: WebDriver):
        """
        Constructor.
        :param name: Session name.
        :param web_driver: Web driver (browser) associated with session
        """
        self._name = name
        self._web_driver = web_driver

    def get_name(self) -> str:
        """
        Get session name
        :return: session name
        """
        return self._name

    def get_web_driver(self) -> WebDriver:
        """
        Get web driver (browser) associated with session
        :return: web driver (browser)
        """
        return self._web_driver


