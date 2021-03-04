from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from server import log
from server.models.register_models import register_models
from celery import Celery

cors = CORS()
db = SQLAlchemy()
celery = Celery(__name__, include=['server.celery_tasks.tasks'])
register_models()
logger = log.get_logger(__name__)
