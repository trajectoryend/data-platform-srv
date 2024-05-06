import configparser
import os


conf = configparser.ConfigParser()
cur_path = os.path.dirname(os.path.realpath(__file__))
config_url = os.path.join(os.path.split(cur_path)[0], 'config.ini')
print(config_url)

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


DEBUG = get_value_from_env('DEBUG', 'system', 'DEBUG', False)
REDIS_PASSWORD = get_value_from_env('REDIS_PASSWORD', 'redis', 'REDIS_PASSWORD', '')
REDIS_HOST = get_value_from_env('REDIS_HOST', 'redis', 'REDIS_HOST', '')
REDIS_PORT = get_value_from_env('REDIS_PORT', 'redis', 'REDIS_PORT', '6379')
DEFAULT_CACHE_ID = get_value_from_env('DEFAULT_CACHE_ID', 'redis', 'DEFAULT_CACHE_ID', '1')
CHANNEL_LAYERS_CACHE_ID = get_value_from_env('CHANNEL_LAYERS_CACHE_ID', 'redis', 'CHANNEL_LAYERS_CACHE_ID', '2')
CELERY_BROKER_CACHE_ID = get_value_from_env('CELERY_BROKER_CACHE_ID', 'redis', 'CELERY_BROKER_CACHE_ID', '3')
