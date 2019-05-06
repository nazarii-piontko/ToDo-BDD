from typing import NoReturn, Union, Sequence

from selenium.webdriver.remote.webelement import WebElement

from infrastructure.config import Config
from infrastructure.config_keys import WellKnownConfigKeys
from infrastructure.errors import TestError
from infrastructure.registry import Registry
from infrastructure.page import Page
from infrastructure.utils import execute_with_retry


class HomePage(Page):
    """
    Base class for page accessor.
    """
    def __init__(self, registry: Registry):
        """
        Constructor.
        :param registry: Services registry.
        """
        Page.__init__(self, registry)

    def navigate(self) -> NoReturn:
        """
        Navigate to page.
        """
        self._navigate('')

    def get_loading_element(self) -> Union[WebElement, None]:
        element = self.get_element_by_css('span.loading')

        if element is not None:
            element = self.get_element_parent(element)

        return element

    def get_welcome_message_element(self) -> Union[WebElement, None]:
        element = self.get_element_by_css('span.pulse')

        if element is not None:
            element = self.get_element_parent(element)

        return element

    def get_todo_items(self) -> Sequence[str]:
        elements = self.get_elements_by_css('li.list-group-item > p')
        todo_items = [e.text for e in elements]
        return todo_items

    def get_todo_items_count(self) -> int:
        elements = self.get_elements_by_css('li.list-group-item > p')
        return len(elements)

    def get_todo_item_by_content(self, todo) -> Union[WebElement, None]:
        elements = self.get_elements_by_css('li.list-group-item > p')
        for element in elements:
            if element.text == todo:
                return self.get_element_parent(element)
        return None

    def add_todo_item(self, todo) -> NoReturn:
        input_field = self.get_element_by_css('#todoInput')
        if input_field is None:
            raise TestError('Unable to find input for new ToDo item')

        input_field.send_keys(todo)

        submit_button = self.get_element_by_css('form > div > button')
        if submit_button is None:
            raise TestError('Unable to find submit button to create new ToDo item')

        current_todo_items_count = self.get_todo_items_count()
        
        submit_button.click()

        execute_with_retry(lambda: self.get_todo_items_count() == current_todo_items_count,
                           timeout=self._registry[Config].get_float(WellKnownConfigKeys.HTTP_WAIT_TIMEOUT))

    def remove_todo_item(self, todo) -> NoReturn:
        todo_element = self.get_todo_item_by_content(todo)
        if todo_element is None:
            raise TestError('ToDo item "{}" is missing'.format(todo))

        remove_button = todo_element.find_element_by_xpath('div/button[2]')
        if remove_button is None:
            raise TestError('Remove button for ToDo item "{}" is missing'.format(todo))

        current_todo_items_count = self.get_todo_items_count()

        remove_button.click()

        execute_with_retry(lambda: self.get_todo_items_count() == current_todo_items_count,
                           timeout=self._registry[Config].get_float(WellKnownConfigKeys.HTTP_WAIT_TIMEOUT))

    def toggle_todo_item_done(self, todo) -> NoReturn:
        todo_element = self.get_todo_item_by_content(todo)
        if todo_element is None:
            raise TestError('ToDo item "{}" is missing'.format(todo))

        toggle_button = todo_element.find_element_by_xpath('div/button[1]')
        if toggle_button is None:
            raise TestError('Toggle button for ToDo item "{}" is missing'.format(todo))

        toggle_button.click()

        execute_with_retry(lambda: not self.is_todo_item_done(todo),
                           timeout=self._registry[Config].get_float(WellKnownConfigKeys.HTTP_WAIT_TIMEOUT))

    def is_todo_item_done(self, todo):
        todo_element = self.get_todo_item_by_content(todo)
        if todo_element is None:
            raise TestError('ToDo item "{}" is missing'.format(todo))

        toggle_button = todo_element.find_element_by_xpath('div/button[1]')
        toggle_button_class = toggle_button.get_attribute('class')
        return 'btn-success' in toggle_button_class
