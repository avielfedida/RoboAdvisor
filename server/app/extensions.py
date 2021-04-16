from flask_cors import CORS
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
import log
from models.register_models import register_models

cors = CORS()
mail = Mail()
db = SQLAlchemy()
register_models()
logger = log.get_logger(__name__)
