from logging import getLogger

from behave.log_capture import capture
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver

from infrastructure.app_controller import AppController
from infrastructure.artifacts import Artifacts
from infrastructure.config import Config
from infrastructure.di import Registry
from infrastructure.web_driver_factory import WebDriverFactory
from infrastructure.utils import get_registry, set_registry


# noinspection PyUnusedLocal
from pages.home_page import HomePage


@capture
def before_all(context):
    registry = Registry()
    config = Config()
    logger = getLogger()

    registry.set(logger)
    registry.set(config)
    registry.set(Artifacts(config))
    registry.set(WebDriverFactory(config))
    registry.set(AppController(config, logger))

    set_registry(context, registry)


# noinspection PyUnusedLocal
@capture
def before_feature(context, feature):
    pass


# noinspection PyUnusedLocal
@capture
def before_scenario(context, scenario):
    registry = get_registry(context)

    registry.get(AppController).start()

    registry.set(registry.get(WebDriverFactory).create(), RemoteWebDriver)

    for page_type in PAGES:
        registry.set(page_type(registry))

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
    registry = get_registry(context)

    registry.get(RemoteWebDriver).quit()
    registry.remove(RemoteWebDriver)

    registry.get(AppController).stop()

    for page_type in PAGES:
        registry.remove(page_type)


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
