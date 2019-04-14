from typing import NoReturn, Union

from selenium.webdriver.remote.webelement import WebElement

from asserts.general import GeneralAssert


class HtmlElementAssert:
    """
    Assert for validation HTML element's state
    """

    def __init__(self, general_assert: GeneralAssert):
        self._general_assert = general_assert

    def assert_visible(self,
                       element: WebElement,
                       message: Union[str, None] = None) -> NoReturn:
        """
        Check is HTML element is visible
        """

        if message is None:
            message = 'HTML element "{}" expected as visible but it is hidden'.format(element)

        self._general_assert.assertTrue(element is not None and element.is_displayed(), message)

    def assert_hidden(self,
                      element: WebElement,
                      message: Union[str, None] = None) -> NoReturn:
        """
        Check is HTML element is hidden
        """

        if message is None:
            message = 'HTML element "{}" expected as hidden but it is visible'.format(element)

        self._general_assert.assertFalse(element is not None and element.is_displayed(), message)
