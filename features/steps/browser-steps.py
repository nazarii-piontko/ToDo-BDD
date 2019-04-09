from behave import *
from time import sleep
from infrastucture.testing_context import TestingContext
use_step_matcher("re")


@when(u'(?:I )?open web page "(?P<path>.+)"')
def open_web_page(context, path):
    c: TestingContext = context.context
    uri = c.get_uri(path)
    c.get_web_driver().get(uri)


@when(u'(?:I )?wait for (?P<sec>\\d+) seconds')
def wait(context, sec):
    sec = int(sec)
    assert sec > 0
    sleep(sec)


@then(u'(?:I should see )?element with css selector "(?P<css_path>.+)" (?P<visibility>(?:visible|hidden))')
def wait(context, css_path, visibility):
    c: TestingContext = context.context
    driver = c.get_web_driver()
    element = driver.find_element_by_css_selector(css_path)
    if visibility == 'visible':
        assert element.is_displayed(), \
            'HTML element with css path "{}" is expected as visible but it is hidden'.format(css_path)
    else:
        assert not element.is_displayed(), \
            'HTML element with css path "{}" is expected as hidden but it is visible'.format(css_path)
