from logging import getLogger

from behave.log_capture import capture
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver

from asserts.general import GeneralAssert
from asserts.html_element import HtmlElementAssert
from infrastructure.app_controller import AppController
from infrastructure.artifacts import Artifacts
from infrastructure.config import Config
from infrastructure.di import Registry, reg, set_registry
from infrastructure.web_driver_factory import WebDriverFactory

# noinspection PyUnusedLocal
from pages.home_page import HomePage


@capture
def before_all(context):
    r = Registry()
    config = Config()
    logger = getLogger()

    r.set(logger)
    r.set(config)
    r.set(Artifacts(config))
    r.set(WebDriverFactory(config))
    r.set(AppController(config, logger))

    r.set(GeneralAssert())
    r.set(HtmlElementAssert(r[GeneralAssert]))

    set_registry(context, r)


# noinspection PyUnusedLocal
@capture
def before_feature(context, feature):
    pass


# noinspection PyUnusedLocal
@capture
def before_scenario(context, scenario):
    r = reg(context)

    r.get(AppController).start()

    r.set(r.get(WebDriverFactory).create(), RemoteWebDriver)

    for page_type in PAGES:
        r.set(page_type(r))

# noinspection PyUnusedLocal
@capture
def before_step(context, step):
    pass


# noinspection PyUnusedLocal
@capture
def after_step(context, step):
    pass


# noinspection PyUnusedLocal
@capture
def after_scenario(context, scenario):
    r = reg(context)

    r.get(RemoteWebDriver).quit()
    r.remove(RemoteWebDriver)

    r.get(AppController).stop()

    for page_type in PAGES:
        r.remove(page_type)


# noinspection PyUnusedLocal
@capture
def after_feature(context, feature):
    pass


# noinspection PyUnusedLocal
@capture
def after_all(context):
    pass


PAGES = [
    HomePage
]
