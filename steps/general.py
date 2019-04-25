from behave import *

from infrastructure.registry import reg
from infrastructure.page import Page

use_step_matcher('re')


@when(u'(?:I )?wait for {seconds:d}')
@then(u'(?:I )?wait for {seconds:d}')
def wait(context, seconds):
    reg(context)[Page].wait(float(seconds))


@when(u'(?:I )?create screenshot')
@then(u'(?:I )?create screenshot')
def create_screenshot(context):
    reg(context)[Page].create_screenshot()
