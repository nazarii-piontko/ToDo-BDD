from behave import *

from pages.home_page import HomePage
from infrastructure.utils import get_registry

use_step_matcher("re")


@when(u'(?:I )?open home page')
def open_home_page(context):
    get_registry(context).get(HomePage).navigate()


@when(u'(?:I )?wait for (?P<seconds>\\d+) seconds')
def wait(context, seconds):
    get_registry(context).get(HomePage).wait(float(seconds))


@then(u'(?:I )?create screenshot')
def create_screenshot(context):
    get_registry(context).get(HomePage).create_screenshot()


@then(u'(?:I should see )?element c"(?P<css_path>.+)" (?P<visibility>(?:visible|hidden))')
def element_with_css_selector_visible_or_hidden(context, css_path, visibility):
    element = get_registry(context).get(HomePage).get_element_by_css(css_path)

    if element is None:
        assert False, 'Element "{}" is missing'.format(css_path)

    if visibility == 'visible':
        assert element.is_displayed(), \
            'HTML element with css path "{}" is expected as visible but it is hidden'.format(css_path)
    else:
        assert not element.is_displayed(), \
            'HTML element with css path "{}" is expected as hidden but it is visible'.format(css_path)
