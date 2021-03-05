import json

from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

from api.algorithms import get_risk_horizon_score, check_if_all_questions_with_answers
from api.markowitz import Markowitz
from api.utils import exceptions_mapper, json_abort, plt_to_src
from app.configurations import Config
from app.extensions import db
from models.results import Results
from celery_tasks.tasks import execute_analysis

class CeleryDemo(MethodView):

    def post(self):
        task = execute_analysis.apply_async(args=[1, 2])
        return make_response(jsonify(message="OK"), 200)


api = Blueprint("celery_demo_api", __name__, url_prefix=Config.API_PREFIX + '/celey_demo')
celery_demo = CeleryDemo.as_view('api_celery_demo')
api.add_url_rule('/', methods=['POST'], view_func=celery_demo)
