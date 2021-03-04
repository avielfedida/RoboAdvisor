from flask import Flask

from app.configurations import Config
from app.extensions import db

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    from app.extensions import cors
    cors.init_app(app)

    # Set up database
    db.init_app(app)

    from api.form_submit import api as demo_api
    from api.celery_demo import api as celery_demo_api
    app.register_blueprint(demo_api)
    app.register_blueprint(celery_demo_api)

    # Create tables
    with app.app_context():
        db.create_all()
        return app
