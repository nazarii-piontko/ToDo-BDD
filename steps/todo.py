from behave import *

from asserts.general import GeneralAssert
from asserts.html_element import HtmlElementAssert
from infrastructure.config import Config
from infrastructure.config_keys import WellKnownConfigKeys
from infrastructure.di import reg
from infrastructure.utils import execute_with_retry
from pages.home_page import HomePage


@given('I open home page')
@given('open home page')
@when('I open home page')
@when('open home page')
def open_home_page(context):
    reg(context)[HomePage].navigate()


@given('I wait until loading is done')
@given('wait until loading is done')
@when('I wait until loading is done')
@when('wait until loading is done')
def wait_until_loading_disappear(context):
    r = reg(context)
    timeout = r[Config].get_float(WellKnownConfigKeys.HTTP_WAIT_TIMEOUT)

    def is_loading_visible():
        loading_element = r[HomePage].get_loading_element()
        return loading_element is not None and loading_element.is_displayed()

    try:
        execute_with_retry(lambda: is_loading_visible(),
                           timeout=timeout)
    except TimeoutError:
        r[GeneralAssert].fail('Loading element is not disappeared in {} seconds'.format(timeout))


@when('I add ToDo item "{todo}"')
@when('add ToDo item "{todo}"')
def add_todo_item(context, todo):
    reg(context)[HomePage].add_todo_item(todo)


@when('I add ToDo items')
@when('add ToDo items')
def add_todo_items(context):
    new_todo_items = context.text.splitlines()

    for item in new_todo_items:
        reg(context)[HomePage].add_todo_item(item)


@when('I remove ToDo item "{todo}"')
@when('remove ToDo item "{todo}"')
def remove_todo_item(context, todo):
    reg(context)[HomePage].remove_todo_item(todo)


@when('I toggle ToDo item "{todo}" to done')
@when('toggle ToDo item "{todo}" to done')
def toggle_todo_item_to_done(context, todo):
    reg(context)[HomePage].toggle_todo_item_done(todo)


@then('I should see welcome message')
@then('see welcome message')
def welcome_message_visible(context):
    r = reg(context)

    welcome_message_element = r[HomePage].get_welcome_message_element()

    r[HtmlElementAssert].assert_visible(welcome_message_element,
                                        'Welcome message is not visible')


@then('I should see ToDo item "{expected_todo}" in the list')
@then('see ToDo item "{expected_todo}" in the list')
def see_todo_item_in_the_list(context, expected_todo):
    r = reg(context)

    actual_todo_items = r[HomePage].get_todo_items()

    r[GeneralAssert].assertIn(expected_todo,
                              actual_todo_items,
                              'ToDo item "{}" is not is the list: {}'.format(expected_todo,
                                                                             '\n'.join(actual_todo_items)))


@then('I should see ToDo items')
@then('see ToDo items')
def see_todo_items(context):
    r = reg(context)

    expected_todo_items = context.text.splitlines()
    actual_todo_items = r[HomePage].get_todo_items()

    r[GeneralAssert].assertSequenceEqual(expected_todo_items,
                                         actual_todo_items,
                                         'ToDo items do not match\nExpected:\n{}\n\nActual:\n{}'
                                         .format('\n'.join(expected_todo_items), '\n'.join(actual_todo_items)))


@then('I should see ToDo item "{todo}" toggled as done')
@then('see ToDo item "{todo}" toggled as done')
def todo_item_should_be_toggled_as_done(context, todo):
    r = reg(context)

    is_done = r[HomePage].is_todo_item_done(todo)

    r[GeneralAssert].assertTrue(is_done, 'ToDo item "{}" is not done'.format(todo))
