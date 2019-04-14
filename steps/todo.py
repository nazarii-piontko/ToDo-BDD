from behave import *

from asserts.general import GeneralAssert
from asserts.html_element import HtmlElementAssert
from infrastructure.config import Config
from infrastructure.config_keys import WellKnownConfigKeys
from infrastructure.di import reg, Registry
from infrastructure.utils import execute_with_retry
from pages.home_page import HomePage


@given('I open home page')
@given('open home page')
@when('I open home page')
@when('open home page')
def open_home_page(context):
    reg(context).get(HomePage).navigate()


@when('I add todo item "{todo}"')
@when('add todo item "{todo}"')
def add_todo_item(context, todo):
    r = reg(context)

    r[HomePage].add_todo_item(todo)


@when('I add todo items')
@when('add todo items')
def add_todo_items(context):
    r = reg(context)

    new_todo_items = context.text.splitlines()

    home_page = r[HomePage]

    for todo in new_todo_items:
        home_page.add_todo_item(todo)


@when('I remove todo item "{todo}"')
@when('remove todo item "{todo}"')
def remove_todo_item(context, todo):
    r = reg(context)
    r[HomePage].remove_todo_item(todo)


@when('I toggle todo item "{todo}" done')
@when('toggle todo item "{todo}" done')
def toggle_todo_item_done(context, todo):
    r = reg(context)
    r[HomePage].toggle_todo_item_done(todo)


@given('wait until loading disappear')
def wait_until_loading_disappear(context):
    r = reg(context)

    timeout = r[Config].get_float(WellKnownConfigKeys.HTTP_WAIT_TIMEOUT)

    try:
        execute_with_retry(lambda: _is_loading_visible(r),
                           timeout=timeout)
    except TimeoutError:
        r[GeneralAssert].fail('Loading element is not disappeared in {} seconds'.format(timeout))


@then('I should see welcome message')
@then('see welcome message')
def welcome_message_visible(context):
    r = reg(context)

    welcome_message_element = r[HomePage].get_welcome_message_element()

    r[HtmlElementAssert].assert_visible(welcome_message_element, 'Welcome message is not visible')


@then('I should see todo item "{expected_todo}" in the list')
@then('see todo item "{expected_todo}" in the list')
def see_todo_item_in_the_list(context, expected_todo):
    r = reg(context)

    actual_todo_items = r[HomePage].get_todo_items()

    r[GeneralAssert].assertIn(expected_todo,
                              actual_todo_items,
                              'ToDo item "{}" is not is the list: {}'.format(expected_todo,
                                                                             '\n'.join(actual_todo_items)))


@then('I should see todo items')
@then('see todo items')
def see_todo_items(context):
    r = reg(context)

    expected_todo_items = context.text.splitlines()
    action_todo_items = r[HomePage].get_todo_items()

    r[GeneralAssert].assertSequenceEqual(expected_todo_items,
                                         action_todo_items,
                                         'ToDo items do not match\nExpected:\n{}\n\nActual:\n{}'
                                         .format('\n'.join(expected_todo_items), '\n'.join(action_todo_items)))


@then('I should see todo item "{todo}" toggled as done')
@then('see todo item "{todo}" toggled as done')
def todo_item_should_be_toggled_as_done(context, todo):
    r = reg(context)

    is_done = r[HomePage].is_todo_item_done(todo)

    r[GeneralAssert].assertTrue(is_done, 'ToDo item "{}" is not done'.format(todo))


def _is_loading_visible(r: Registry):
    loading_element = r[HomePage].get_loading_element()

    return loading_element is not None and loading_element.is_displayed()
