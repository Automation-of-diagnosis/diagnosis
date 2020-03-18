import logging
from typing import Dict, List, Union

DB_NAME: str = "my_app.db"

LOGGING: Dict[str, Union[int, str, Dict[str, List]]] = {
    'version': 1,

    'formatters': {
        'default': {
            'format': '[%(asctime)s] [%(levelname)s] - %(name)s: %(message)s',
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
