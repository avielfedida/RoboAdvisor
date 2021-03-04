import json

from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

from server.api.algorithms import get_risk_horizon_score, check_if_all_questions_with_answers
from server.api.markowitz import Markowitz
from server.api.utils import exceptions_mapper, json_abort, plt_to_src
from server.app.configurations import Config
from server.app.extensions import db
from server.models.results import Results
from server.celery_tasks.tasks import execute_analysis

class CeleryDemo(MethodView):

    def post(self):
        task = execute_analysis.apply_async(args=[1, 2])
        return make_response(jsonify(message="OK"), 200)


api = Blueprint("celery_demo_api", __name__, url_prefix=Config.API_PREFIX + '/celey_demo')
celery_demo = CeleryDemo.as_view('api_celery_demo')
api.add_url_rule('/', methods=['POST'], view_func=celery_demo)
