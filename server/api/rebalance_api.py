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
        try:
            data = request.get_json()
            link = data.get("link")
            portfolio_by_algorithm = db.session.query(Portfolio).filter_by(link=link).first()
            algo = create_model(portfolio_by_algorithm.algorithm, portfolio_by_algorithm.risk)
            portfolio = algo.rebalance(link)
            for pk_of_risk in get_next_answer_set_pk(portfolio_by_algorithm.risk):
                pua = PortUserAnswersSet(user_id=curr_user.id, ans_set_val=pk_of_risk, portfolios_id=portfolio.id,
                                         portfolios_date_time=portfolio.date_time)
                db.session.add(pua)
            db.session.add(portfolio)
            db.session.commit()
            response = make_response(jsonify(message="חישוב התיק מחדש הסתיים בהצלחה", new_link=portfolio.link), 200)
        except Exception as e:
            response = make_response(jsonify(message=str(e)), 400)
        return response


api = Blueprint('rebalance_api', __name__, url_prefix=Config.API_PREFIX + '/rebalance')
rebalance = RebalanceApi.as_view('rebalance_api')
api.add_url_rule('/rebalanced', methods=['POST'], view_func=rebalance)
