from flask import Flask


def create_app(config_name="development"):
    app = Flask(__name__)
    from app.extensions import cors
    cors.init_app(app)
    return app
