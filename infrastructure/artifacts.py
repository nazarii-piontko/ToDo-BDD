from typing import NoReturn
from os import path, makedirs

from infrastructure.errors import TestError
from infrastructure.config import Config, WellKnownConfigKeys


class Artifacts:
    """
    Provider artifacts functionality.
    """
    def __init__(self, config: Config):
        """
        Constructor.
        :param config: Configuration.
        """
        self.__config = config
        self.__init_dirs()

    def get_artifacts_dir(self) -> str:
        """
        Get artifacts dir path
        """
        return self.__config.get(WellKnownConfigKeys.ARTIFACTS_DIR)

    def __init_dirs(self) -> NoReturn:
        artifacts_dir = self.get_artifacts_dir()

        if artifacts_dir is None:
            raise TestError('Missing artifacts directory in configuration')

        if not path.exists(artifacts_dir):
            makedirs(artifacts_dir)
