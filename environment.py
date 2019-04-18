from logging import getLogger

from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver

from asserts.general import GeneralAssert
from asserts.html_element import HtmlElementAssert
from infrastructure.app_controller import AppController
from infrastructure.artifacts import Artifacts
from infrastructure.config import Config
from infrastructure.config_providers import EnvironmentConfigProvider, JsonConfigProvider
from infrastructure.di import Registry, reg, set_registry
from infrastructure.web_driver_factory import WebDriverFactory
from pages import PAGES


# noinspection PyUnusedLocal
def before_all(context):
    r = Registry()

    config = Config([EnvironmentConfigProvider(), JsonConfigProvider('./config.json')])
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
def before_feature(context, feature):
    pass


# noinspection PyUnusedLocal
def before_scenario(context, scenario):
    r = reg(context)

    r.get(AppController).start()

    r.set(r.get(WebDriverFactory).create(), RemoteWebDriver)

    for page_type in PAGES:
        r.set(page_type(r))


# noinspection PyUnusedLocal
def before_step(context, step):
    pass


# noinspection PyUnusedLocal
def after_step(context, step):
    pass


# noinspection PyUnusedLocal
def after_scenario(context, scenario):
    r = reg(context)

    r.get(RemoteWebDriver).quit()
    r.remove(RemoteWebDriver)

    r.get(AppController).stop()

    for page_type in PAGES:
        r.remove(page_type)


# noinspection PyUnusedLocal
def after_feature(context, feature):
    pass


# noinspection PyUnusedLocal
def after_all(context):
    pass
