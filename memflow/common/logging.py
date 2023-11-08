import os

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - [%(threadName)s] - %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'default',
        },
        'file': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'level': 'INFO',
            'formatter': 'default',
            'filename': f"{os.environ.get('WORKDIR')}/logs/app.log",
            'when': 'D',
            'interval': 1,
            'backupCount': 7,
        },
    },
    'loggers': {
        '': {  # root logger
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True,
        },
        'apscheduler': {  # Specific logger for apscheduler
            'handlers': ['console', 'file'],
            'level': 'ERROR',  # Set to WARNING to suppress INFO and DEBUG messages
            'propagate': False,  # Do not propagate to root logger
        },
        'httpx': {  # Specific logger for httpx
            'handlers': ['console', 'file'],
            'level': 'ERROR',  # Set to WARNING to suppress INFO and DEBUG messages
            'propagate': False,  # Do not propagate to root logger
        },
    }
}
