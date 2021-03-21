import json
from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from app.configurations import Config
from celery_tasks.tasks import print_hello
import celery_tasks.tasks as tasks



class CeleryDemo(MethodView):

    def post(self):
        tasks.insert_price_data()
        # tasks.print_hello()
        # print_hello.apply_async()#args=[alg.as_dict(), analysis_type, params]) # No args for now
        return make_response(jsonify(message="OK"), 200)


api = Blueprint("celery_demo_api", __name__, url_prefix=Config.API_PREFIX + '/celey_demo')
celery_demo = CeleryDemo.as_view('api_celery_demo')
api.add_url_rule('/', methods=['POST'], view_func=celery_demo)
