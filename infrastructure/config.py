from typing import Union
from os import environ


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
        return value == 'True'


class WellKnownConfigKeys:
    """
    Well known config keys.
    """
    APP_BASE_URI = 'APP_BASE_URI'
    APP_PROBE_URI = 'APP_PROBE_URI'
    APP_DOCKER_COMPOSE_FILE = 'APP_DOCKER_COMPOSE_FILE'
    SELENIUM_REMOTE = 'SELENIUM_REMOTE'
    SELENIUM_REMOTE_URI = 'SELENIUM_REMOTE_URI'
    SELENIUM_DRIVER = 'SELENIUM_DRIVER'
    ARTIFACTS_DIR = 'ARTIFACTS_DIR'
    WAIT_TIMEOUT = 'WAIT_TIMEOUT'


"""
Default config values.
"""
DEFAULT_CONFIG_VALUES = {
    WellKnownConfigKeys.APP_BASE_URI: 'http://localhost/',
    WellKnownConfigKeys.APP_PROBE_URI: 'http://localhost/',
    WellKnownConfigKeys.APP_DOCKER_COMPOSE_FILE: './app/docker-compose.yml',
    WellKnownConfigKeys.SELENIUM_REMOTE: 'False',
    WellKnownConfigKeys.SELENIUM_REMOTE_URI: 'http://localhost:4444/wd/hub',
    WellKnownConfigKeys.SELENIUM_DRIVER: 'chrome',  # chrome or firefox
    WellKnownConfigKeys.ARTIFACTS_DIR: './artifacts',
    WellKnownConfigKeys.WAIT_TIMEOUT: '60'
}
