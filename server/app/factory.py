from flask import Flask
from .configurations import Config
from .extensions import db
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

    # We created these APIs to perform database-based testing
    from api.users_api import api as users_api
    from api.members_api import api as members_api
    from api.stocks_prices_api import api as stocks_prices_api
    from api.portfolio_api import api as portfolio_api
    from api.answers_set_api import api as answers_set_api
    from api.port_user_answers_set_api import api as port_user_answers_set_api
    from api.portfolio_stocks_api import api as portfolio_stocks_api
    from api.clusters_api import api as clusters_api
    from api.topics_api import api as topics_api
    from api.messages_api import api as messages_api
    from api.stock_prices_data_insert_api import api as stock_prices_data_insert_api
    from api.algorithm_api import api as algorithm_api
    from api.form_submit import api as submit_form_api

    app.register_blueprint(users_api)
    app.register_blueprint(members_api)
    app.register_blueprint(stocks_prices_api)
    app.register_blueprint(portfolio_api)
    app.register_blueprint(answers_set_api)
    app.register_blueprint(port_user_answers_set_api)
    app.register_blueprint(portfolio_stocks_api)
    app.register_blueprint(clusters_api)
    app.register_blueprint(topics_api)
    app.register_blueprint(messages_api)
    app.register_blueprint(algorithm_api)
    app.register_blueprint(submit_form_api)
    app.register_blueprint(stock_prices_data_insert_api)

    # Create tables
    with app.app_context():
        db.create_all()
        return app
