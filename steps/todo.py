from behave import *

from asserts.general import GeneralAssert
from asserts.html_element import HtmlElementAssert
from pages.home_page import HomePage
from infrastructure.di import reg

use_step_matcher("re")


@when(u'(?:I )?open home page')
def open_home_page(context):
    reg(context).get(HomePage).navigate()


@when(u'(?:I )?wait for (?P<seconds>\\d+) seconds')
def wait(context, seconds):
    reg(context).get(HomePage).wait(float(seconds))


@then(u'(?:I )?create screenshot')
def create_screenshot(context):
    reg(context).get(HomePage).create_screenshot()


@then(u'(?:I should see )?element c"(?P<css_path>.+)" (?P<visibility>(?:visible|hidden))')
def element_with_css_selector_visible_or_hidden(context, css_path, visibility):
    r = reg(context)

    element = r[HomePage].get_element_by_css(css_path)

    r[GeneralAssert].assertIsNotNone(element, 'Element "{}" is missing'.format(css_path))

    if visibility == 'visible':
        r[HtmlElementAssert].assert_visible(element,
                                            'HTML element with css path "{}" is expected as visible but it is hidden'
                                            .format(css_path))
    else:
        r[HtmlElementAssert].assert_hidden(element,
                                           'HTML element with css path "{}" is expected as hidden but it is visible'
                                           .format(css_path))
