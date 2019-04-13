from typing import NoReturn, Union
from logging import Logger
from subprocess import Popen

from infrastructure.utils import is_uri_accessible, execute_with_retry
from infrastructure.errors import TestError
from infrastructure.config import Config
from infrastructure.config_keys import WellKnownConfigKeys


class AppController:
    """
    Controller which is responsible for control of lifecycle of application under the test.
    """
    def __init__(self, config: Config, logger: Logger):
        """
        Constructor.
        :param config: Configuration.
        :param logger: Logger.
        """
        self._logger = logger
        self._config = config

    def start(self) -> NoReturn:
        """
        Start the application under the test
        """
        docker_compose_file = self._config.get(WellKnownConfigKeys.APP_DOCKER_COMPOSE_FILE)
        docker_process: Union[Popen, None]

        if docker_compose_file is None:
            self._logger.debug('app_controller: docker-compose file is missing in configuration')
            docker_process = None
        else:
            docker_process = self._run_docker_compose_up(docker_compose_file)

        execute_with_retry(lambda: not self._is_app_accessible(docker_process),
                           timeout=self._config.get_float(WellKnownConfigKeys.WAIT_TIMEOUT))

    def stop(self) -> NoReturn:
        """
        Stop the application under the test
        """
        docker_compose_file = self._config.get(WellKnownConfigKeys.APP_DOCKER_COMPOSE_FILE)

        if docker_compose_file is None:
            return

        docker_process = self._run_docker_compose_down(docker_compose_file)
        execute_with_retry(lambda: docker_process.poll() is None,
                           timeout=self._config.get_float(WellKnownConfigKeys.WAIT_TIMEOUT))

    def get_uri(self) -> str:
        """
        Get application base URI
        :return:
        """
        return self._config.get(WellKnownConfigKeys.APP_BASE_URI)

    def _run_docker_compose_up(self, docker_compose_file: str) -> Popen:
        """
        Start docker-compose up process
        :param docker_compose_file: docker-compose.yml path.
        :return: Process of docker-compose.
        """
        command = 'docker-compose -f "{}" up -d'.format(docker_compose_file)

        process = Popen(command, shell=True)

        return process

    def _run_docker_compose_down(self, docker_compose_file: str) -> Popen:
        """
        Start docker-compose down process
        :param docker_compose_file: docker-compose.yml path.
        :return: Process of docker-compose.
        """
        command = 'docker-compose -f "{}" down'.format(docker_compose_file)

        process = Popen(command, shell=True)

        return process

    def _is_app_accessible(self, docker_process: Union[Popen, None]) -> bool:
        """
        Check is application is accessible by accessing application probe URL
        :param docker_process: Docker process to check if there is no fail
        :return: True is application is accessible, False - otherwise
        """
        if docker_process is not None \
                and docker_process.poll() is not None \
                and docker_process.returncode != 0:
            raise TestError('Unable to execute docker-compose')

        is_accessible = is_uri_accessible(self._config.get(WellKnownConfigKeys.APP_PROBE_URI))
        return is_accessible
