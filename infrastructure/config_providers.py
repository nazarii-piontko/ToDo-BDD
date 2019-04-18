from os import environ, path
from typing import Union
from json import load as json_load


class ConfigProvider:
    """
    Base class for configuration provider
    """
    def get(self, key: str) -> Union[str, None]:
        """
        Return value by key if it is exists, otherwise - None
        :param key: Key.
        :return: Value or None.
        """
        raise NotImplementedError()


class EnvironmentConfigProvider(ConfigProvider):
    """
    Configuration provider which uses environment variables as source of configuration
    """
    def __init__(self, env_prefix: str = ''):
        """
        Constructor.
        :param env_prefix: Optional prefix for names of environmental variables
        """
        self.env_prefix = env_prefix

    def get(self, key: str) -> Union[str, None]:
        env_key = self.env_prefix + key

        if env_key in environ:
            return environ[env_key]
        return None


class JsonConfigProvider(ConfigProvider):
    """
    Configuration provider which uses json file as source of configuration
    """
    def __init__(self, json_file_path: str):
        """
        Constructor.
        :param json_file_path: Path for json file with configuration
        """
        if path.exists(json_file_path):
            with open(json_file_path, 'r') as json_file:
                self.config = json_load(json_file)
        else:
            self.config = None

    def get(self, key: str) -> Union[str, None]:
        if self.config is not None and key in self.config:
            return str(self.config[key])
        return None
