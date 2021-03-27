import json
from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from app.configurations import Config
from celery_tasks.tasks import insert_price_data


class CeleryDemo(MethodView):

    def post(self):
        insert_price_data()
        # insert_price_data.apply_async()  # args=[alg.as_dict(), analysis_type, params]) # No args for now
        return make_response(jsonify(message="OK"), 200)


api = Blueprint("celery_demo_api", __name__, url_prefix=Config.API_PREFIX + '/celey_demo')
celery_demo = CeleryDemo.as_view('api_celery_demo')
api.add_url_rule('/', methods=['POST'], view_func=celery_demo)
