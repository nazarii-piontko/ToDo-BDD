from typing import Union


class TestError(Exception):
    """
    Test error
    """
    def __init__(self, message: str, inner_error: Union[Exception, None] = None):
        """
        Constructor.
        :param message: Error message.
        :param inner_error: Inner error/exception.
        """
        self.message = message
        self.inner_error = inner_error

    def __repr__(self):
        """
        String representation.
        :return: String representation.
        """
        message = 'Test Error: {}'.format(self.message)

        if self.inner_error is not None:
            message += ' -> {}'.format(self.inner_error)

        return message
