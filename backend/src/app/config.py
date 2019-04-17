import os

_environment = os.environ.get('ENVIRONMENT', 'default')
_sqlalchemy_database_uri = os.environ['SQLALCHEMY_DATABASE_URI']

_configs = {
    'dev': {
        'ENV': 'development',
        'DEBUG': True,
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': _sqlalchemy_database_uri,
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    },
    'prod': {
        'ENV': 'production',
        'DEBUG': False,
        'TESTING': False,
        'SQLALCHEMY_DATABASE_URI': _sqlalchemy_database_uri,
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    },
    'default': {
        'ENV': 'production',
        'DEBUG': False,
        'TESTING': False,
        'SQLALCHEMY_DATABASE_URI': _sqlalchemy_database_uri,
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    },
}

config = _configs[_environment]
