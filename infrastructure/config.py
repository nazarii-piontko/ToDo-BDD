from typing import Union, Sequence

from infrastructure.config_providers import ConfigProvider


class Config:
    """
    Config class is responsible for providing configurable options for tests
    Values are provided from config providers which probe one by one
    """

    def __init__(self, providers: Sequence[ConfigProvider]):
        """
        Config constructor.
        :param providers: Configuration providers, e.g. env, json file, etc.
        """
        self.providers = providers

    def get(self, key: str, default_value: Union[str, None] = None) -> Union[str, None]:
        """
        Get configurable value by key as str.
        :param key: Config key.
        :param default_value: Default value when key is missing.
        :return: Config value as string.
        """
        for provider in self.providers:
            value = provider.get(key)
            if value is not None:
                return value

        return default_value

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
