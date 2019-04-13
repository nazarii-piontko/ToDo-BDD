from infrastructure.config_keys import WellKnownConfigKeys

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
    WellKnownConfigKeys.WAIT_TIMEOUT: '120'
}
