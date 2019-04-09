from selenium.webdriver import Chrome
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from sys import platform


class WebDriverFactory:
    """
    Encapsulate instantuation of WebDriver based on configuration and environment
    """
    def create(self) -> RemoteWebDriver:

        executable_path = './tools/chromedrivers/'

        if platform == 'linux' or platform == 'linux2':
            executable_path += 'linux'
        elif platform == "darwin":
            executable_path += 'mac'
        elif platform == "win32":
            executable_path += 'win.exe'

        wd = Chrome(executable_path=executable_path)

        return wd