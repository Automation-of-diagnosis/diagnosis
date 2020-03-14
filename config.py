import logging

DB_NAME = "my_app.db"

LOGGING = {
    'version': 1,

    'formatters': {
        'default': {
            'format': '[%(actime)s] [%(levelname)s] - %(name)s: %(message)s',
            },
    },

    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'formatter': 'default',
            'filename': 'my_app.log',
        },
    },

    'loggers': {
        'my_app': {
            'handlers': ['file', ],
            'level': logging.DEBUG
        },
    },
}