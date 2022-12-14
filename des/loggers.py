from logging.config import dictConfig
import logging

dictConfig({
    'version': 1,
    'formatters': {
        'standard': {
            'format': '%(levelname)s :: %(asctime)s : %(filename)s : %(lineno)d : %(message)s'
        }
    },
    'handlers': {
        'file_handler': {
            'class': 'logging.FileHandler',
            'filename': f'./log.log',
            'level': 'DEBUG',
            "encoding": "utf8",
            'formatter': 'standard'
        },
        
    },
    'loggers': {
        'main_logger': {
            'level': 'INFO',
            'handlers': ['file_handler']
        }
    },
})

logger = logging.getLogger("main_logger")

