from flask import Flask


def create_app(config_name="development"):
    app = Flask(__name__)
    from app.extensions import cors
    cors.init_app(app)

    from api.demo import api as demo_api
    app.register_blueprint(demo_api)
    return app
