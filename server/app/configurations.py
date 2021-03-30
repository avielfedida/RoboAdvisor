import os
from datetime import timedelta


class Config(object):
    # Flask
    MODULE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    PROJECT_DIR = os.path.dirname(MODULE_DIR)
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024 * 1024 * 1024
    SECRET_KEY = 'e5ac358c-f0bf-11e5-9e39-d3b532c10a28'

    # Celery configurations
    CELERY_BROKER_URL = 'redis://localhost:6380/0'
    CELERY_RESULT_BACKEND = 'rpc://'
    CELERY_ACCEPT_CONTENT = ['json', 'yaml']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_TIMEZONE = 'Asia/Jerusalem'
    CELERY_ENABLE_UTC = True
    CELERYBEAT_SCHEDULE = {
        'print-hello-every-2-seconds': {
            'task': 'print_hello',  # notice that the complete name is needed
            'schedule': timedelta(seconds=1

                                  ),
            # 'args': (16000, 42) # If needed, commented out for now
        },
    }


    # API
    API_PREFIX = '/api/v1'
    MESSAGES_PER_PAGE = 2
    TOPICS_PER_PAGE = 2

    # Database
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:16941694@127.0.0.1:5432/radb'
    # SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:123@127.0.0.1:5432/radb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
