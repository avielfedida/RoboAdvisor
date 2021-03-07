from flask import Flask

from .configurations import Config
from .extensions import db

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    from app.extensions import cors
    cors.init_app(app)

    # Set up database
    db.init_app(app)

    from api.form_submit import api as sumbit_form
    from api.celery_demo import api as celery_demo_api
    from api.users_api import api as users_api
    from api.stocks_prices_api import api as stocks_prices_api
    app.register_blueprint(sumbit_form)
    app.register_blueprint(celery_demo_api)
    app.register_blueprint(users_api)
    app.register_blueprint(stocks_prices_api)

    # Create tables
    with app.app_context():
        db.create_all()
        return app
