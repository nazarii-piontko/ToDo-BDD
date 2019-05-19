from logging import getLogger

from asserts.general import GeneralAssert
from asserts.html_element import HtmlElementAssert

from infrastructure.app_controller import AppController
from infrastructure.artifacts import Artifacts
from infrastructure.config import Config
from infrastructure.config_providers import EnvironmentConfigProvider, JsonConfigProvider
from infrastructure.registry import Registry, reg, set_registry
from infrastructure.session import Session
from infrastructure.sessions import Sessions
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
    r.set(Sessions())

    r.set(GeneralAssert())
    r.set(HtmlElementAssert(r[GeneralAssert]))

    set_registry(context, r)


# noinspection PyUnusedLocal
def before_feature(context, feature):
    pass


# noinspection PyUnusedLocal
def before_scenario(context, scenario):
    r = reg(context)

    r[AppController].start()

    default_session = Session('default', r[WebDriverFactory].create())
    r[Sessions].add(default_session)

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

    for session in r[Sessions].get_sessions():
        session.get_web_driver().quit()
    r[Sessions].clear()

    r.get(AppController).stop()

    for page_type in PAGES:
        r.remove(page_type)


# noinspection PyUnusedLocal
def after_feature(context, feature):
    pass


# noinspection PyUnusedLocal
def after_all(context):
    pass
