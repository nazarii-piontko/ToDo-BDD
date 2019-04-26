from behave import *

from infrastructure.registry import reg
from infrastructure.page import Page

use_step_matcher('re')


@when(u'(?:I )?wait for (?P<seconds>\\d+) seconds?')
def wait(context, seconds):
    reg(context)[Page].wait(float(seconds))


@when(u'(?:I )?create screenshot')
def create_screenshot(context):
    reg(context)[Page].create_screenshot()
