import configparser
import os


conf = configparser.ConfigParser()
cur_path = os.path.dirname(os.path.realpath(__file__))
config_url = os.path.join(os.path.split(cur_path)[0], 'config.ini')

conf.read(config_url)


def get_value_from_env(env_name, section, option, default_value):
    value = os.environ.get(env_name, None)
    if value:
        return value
    else:
        try:
            return conf.get(section, option)
        except (configparser.NoOptionError, configparser.NoSectionError):
            return default_value


SYSTEM_DEBUG = get_value_from_env('SYSTEM_DEBUG', 'system', 'SYSTEM_DEBUG', False)


REDIS_PASSWORD = get_value_from_env('REDIS_PASSWORD', 'redis', 'REDIS_PASSWORD', '')
REDIS_HOST = get_value_from_env('REDIS_HOST', 'redis', 'REDIS_HOST', '')
REDIS_PORT = get_value_from_env('REDIS_PORT', 'redis', 'REDIS_PORT', '6379')
DEFAULT_CACHE_ID = get_value_from_env(
    'DEFAULT_CACHE_ID', 'redis', 'DEFAULT_CACHE_ID', '1'
)
CHANNEL_LAYERS_CACHE_ID = get_value_from_env(
    'CHANNEL_LAYERS_CACHE_ID', 'redis', 'CHANNEL_LAYERS_CACHE_ID', '2'
)
CELERY_BROKER_CACHE_ID = get_value_from_env(
    'CELERY_BROKER_CACHE_ID', 'redis', 'CELERY_BROKER_CACHE_ID', '3'
)


MYSQL_NAME = get_value_from_env('MYSQL_NAME', 'mysql', 'MYSQL_NAME', '')
MYSQL_USER = get_value_from_env('MYSQL_USER', 'mysql', 'MYSQL_USER', '')
MYSQL_PASSWORD = get_value_from_env('MYSQL_PASSWORD', 'mysql', 'MYSQL_PASSWORD', '')
MYSQL_HOST = get_value_from_env('MYSQL_HOST', 'mysql', 'MYSQL_HOST', '')
MYSQL_PORT = get_value_from_env('MYSQL_PORT', 'mysql', 'MYSQL_PORT', '3306')

WORKFLOW_URL = get_value_from_env('WORKFLOW_URL', 'workflow', 'WORKFLOW_URL', 'http://127.0.0.1')
WORKFLOW_APPNAME = get_value_from_env('WORKFLOW_APPNAME', 'workflow', 'WORKFLOW_APPNAME', '')
WORKFLOW_TOKEN = get_value_from_env('WORKFLOW_TOKEN', 'workflow', 'WORKFLOW_TOKEN', '')
WORKFLOW_ES = get_value_from_env('WORKFLOW_ES', 'workflow', 'WORKFLOW_ES', '')
