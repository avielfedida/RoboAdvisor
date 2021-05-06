from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from app.configurations import Config
from app.extensions import db
from algorithms.create_model import create_model
from datetime import datetime

from models.port_user_answers_set import PortUserAnswersSet


class RebalanceApi(MethodView):

    def get(self, model_name, risk, link, user_id, answer_set, portfolio_id):
        try:
            algo = create_model(model_name, risk)
            portfolio = algo.rebalance(link)
            db.session.add(portfolio)
            user_ans_port = db.session.query(PortUserAnswersSet).filter_by(user_id=user_id, ans_set_val=answer_set, portfolios_id=portfolio_id).first()
            user_ans_port.portfolios_id = portfolio.id
            user_ans_port.portfolios_date_time = portfolio.date_time
            db.session.commit()
            response = make_response(jsonify(message="rebalance ended successfully"), 200)
        except Exception as e:
            response = make_response(jsonify(message=str(e)), 400)
        return response


api = Blueprint('rebalance_api', __name__, url_prefix=Config.API_PREFIX + '/rebalance')
rebalance = RebalanceApi.as_view('rebalance_api')
api.add_url_rule('/rebalanced/<string:model_name>/<int:risk>/<string:link>/<string:user_id>/<string:answer_set>/<int:portfolio_id>', methods=['GET'], view_func=rebalance)
