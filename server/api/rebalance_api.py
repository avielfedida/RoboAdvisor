import uuid

from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

from api.utils import token_required, json_abort, get_next_answer_set_pk
from app.configurations import Config
from app.extensions import db
from algorithms.create_model import create_model
from datetime import datetime

from models.port_user_answers_set import PortUserAnswersSet
from models.portfolio import Portfolio


class RebalanceApi(MethodView):

    @token_required
    def post(self, curr_user):
        from celery_tasks.worker_tasks import execute_rebalance
        try:
            data = request.get_json()
            link = data.get("link")
            if not db.session.query(Portfolio).filter_by(link=link).first():
                return make_response(jsonify(message="לינק לא תקין"), 400)

            execute_rebalance.apply_async(args=[link, curr_user.id])
            response = make_response(jsonify(message="בקשה לחישוב התיק מחדש התקבלה בהצלחה ותעובד בדקות הקרובות"), 200)
        except Exception as e:
            response = make_response(jsonify(message=str(e)), 400)
        return response



api = Blueprint('rebalance_api', __name__, url_prefix=Config.API_PREFIX + '/rebalance')
rebalance = RebalanceApi.as_view('rebalance_api')
api.add_url_rule('/rebalanced', methods=['POST'], view_func=rebalance)
