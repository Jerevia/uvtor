from os.path import abspath, dirname
from os import environ


DEBUG = environ.get('DEBUG') == 'True'

LISTEN_PORT = 8000

COOKIE_SECRET = {cookie_secret}

ROOT_DIR = dirname(abspath(__file__))

ENVS = {{
    'TEST': {{
        'host': '127.0.0.1',
        'port': 5432,
        'user': 'postgres',
        'database': 'postgres',
        'password': 'postgres'
    }},
    'PROD': {{
        'host': '127.0.0.1',
        'port': 5432,
        'user': 'postgres',
        'database': 'postgres',
        'password': 'postgres'
    }}
}}

if DEBUG:
    db = ENVS.get('TEST')

    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    REDIS_DB_INDEX = 4
    REDIS_CONN_POOL_MIN_SIZE = 20
    REDIS_CONN_POOL_MAX_SIZE = 100

    CELERY_BROKER = 'redis://127.0.0.1:6379/5'

    CACHES = {{

        'default': {{
            'cache': 'aiocache.RedisCache',
            'endpoint': '127.0.0.1',
            'port': 6379,
            'db': 4,
            'timeout': 1,
            'serializer': {{
                'class': 'aiocache.serializers.PickleSerializer'
            }},
            'plugins': [
                {{'class': 'aiocache.plugins.HitMissRatioPlugin'}},
                {{'class': 'aiocache.plugins.TimingPlugin'}}
            ]
        }}
    }}

else:
    db = ENVS.get('PROD')

    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    REDIS_DB_INDEX = 4
    REDIS_CONN_POOL_MIN_SIZE = 20
    REDIS_CONN_POOL_MAX_SIZE = 100

    CELERY_BROKER = 'redis://127.0.0.1:6379/5'

    CACHES = {{

        'default': {{
            'cache': 'aiocache.RedisCache',
            'endpoint': '127.0.0.1',
            'port': 6379,
            'db': 4,
            'timeout': 1,
            'serializer': {{
                'class': 'aiocache.serializers.PickleSerializer'
            }},
            'plugins': [
                {{'class': 'aiocache.plugins.HitMissRatioPlugin'}},
                {{'class': 'aiocache.plugins.TimingPlugin'}}
            ]
        }}
    }}

DB_USER = db.get('user')
DB_PASSWORD = db.get('password')
DB_DATABASE = db.get('database')
DB_HOST = db.get('host')
DB_CONN_POOL_MIN_SIZE = 10
DB_CONN_POOL_MAX_SIZE = 100

SESSION_PREFIX = 'SESSION'
LOCK_PREFIX = 'lock'

CAPTCHA_CACHE_PREFIX = 'CAPTCHA'
CAPTCHA_TIMEOUT = 10 * 60
VCODE_CACHE_PREFIX = 'VCODE'
VCODE_TIMEOUT = 10 * 60

# AWS_ACCESS_KEY_ID = 'aws_key'
# AWS_SECRET_ACCESS_KEY = 'access_key'
# AWS_S3_HOST = 's3.cn-north-1.amazonaws.com.cn'

