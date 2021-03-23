from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import log
from models.register_models import register_models
from celery import Celery

cors = CORS()
db = SQLAlchemy()
celery = Celery(__name__, include=['celery_tasks.tasks'])
register_models()
logger = log.get_logger(__name__)
