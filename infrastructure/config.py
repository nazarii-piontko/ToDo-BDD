from os import environ
from typing import Union

from infrastructure.config_default import DEFAULT_CONFIG_VALUES


class Config:
    """
    Config class is responsible for providing configurable options for tests
    Values are provided from environmental or from default values
    """

    def __init__(self, env_prefix: str = ''):
        """
        Config constructor.
        :param env_prefix: prefix for environmental variable.
        """
        self.env_prefix = env_prefix

    def get(self, key: str, default_value: Union[str, None] = None) -> Union[str, None]:
        """
        Get configurable value by key as str.
        :param key: Config key.
        :param default_value: Default value when key is missing.
        :return: Config value as string.
        """

        env_key = self.env_prefix + key
        if env_key in environ:
            value = environ[env_key]
        else:
            value = None

        if value is None:
            if key in DEFAULT_CONFIG_VALUES:
                value = DEFAULT_CONFIG_VALUES[key]
            else:
                value = default_value

        return value

    def get_int(self, key: str, default_value: Union[int, None] = None) -> Union[int, None]:
        """
        Get configurable value by key as int.
        :param key: Config key.
        :param default_value: Default value when key is missing.
        :return: Config value as int.
        """
        value = self.get(key)
        return default_value if value is None else int(value)

    def get_float(self, key: str, default_value: Union[float, None] = None) -> Union[float, None]:
        """
        Get configurable value by key as float.
        :param key: Config key.
        :param default_value: Default value when key is missing.
        :return: Config value as float.
        """
        value = self.get(key)
        return default_value if value is None else float(value)

    def get_bool(self, key: str, default_value: Union[bool, None] = None) -> Union[bool, None]:
        """
        Get configurable value as bool by key.
        :param key: Config key.
        :param default_value: Default value when key is missing.
        :return: Config value as bool.
        """
        value = self.get(key)
        return default_value if value is None else value == 'True'

    def __getitem__(self, key: str) -> Union[str, None]:
        return self.get(key)
