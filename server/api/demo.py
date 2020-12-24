from flask import Blueprint
from flask.views import MethodView


class Demo(MethodView):
    def get(self, name):
        return name, 200


api = Blueprint("api_demo", __name__, url_prefix='/api/v1' + '/demo')
demo = Demo.as_view('demo_api')
api.add_url_rule('/<string:name>', methods=['GET'], view_func=demo)
