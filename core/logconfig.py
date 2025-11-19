import errno
import logging
import os
from logging import config


from config import ROOT_DIR


try:
    os.makedirs(f'{ROOT_DIR}/output')
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

config.dictConfig(
    {
        'version': 1,
        'formatters': {
            'default': {
                'format': '%(asctime)s.%(msecs)03d %(levelname)s %(name)s:%(lineno)s - %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S',
            }
        },
        'handlers': {
            'file': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'default',
                'mode': 'a',
                'filename': f'{ROOT_DIR}/output/test.log',
                'maxBytes': 4000000,
                'backupCount': 0,
            }
        },
        'loggers': {
            'core': {'level': 'DEBUG', 'handlers': ['file']},
            'tests': {'level': 'DEBUG', 'handlers': ['file']},
        },
        'disable_existing_loggers': False,
    }
)


def get_logger(name):
    """All test modules should use this method to get the logger"""
    logger = logging.getLogger(name)
    return logger
