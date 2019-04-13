from typing import NoReturn
from os import path, makedirs

from infrastructure.errors import TestError
from infrastructure.config import Config
from infrastructure.config_keys import WellKnownConfigKeys


class Artifacts:
    """
    Provider artifacts functionality.
    """
    def __init__(self, config: Config):
        """
        Constructor.
        :param config: Configuration.
        """
        self._config = config
        self._init_dirs()

    def get_artifacts_dir(self) -> str:
        """
        Get artifacts dir path
        """
        return self._config.get(WellKnownConfigKeys.ARTIFACTS_DIR)

    def _init_dirs(self) -> NoReturn:
        """
        Create artifacts directory if it is missing
        :return:
        """
        artifacts_dir = self.get_artifacts_dir()

        if artifacts_dir is None:
            raise TestError('Missing artifacts directory in configuration')

        if not path.exists(artifacts_dir):
            makedirs(artifacts_dir)
