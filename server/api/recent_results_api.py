from flask import Blueprint, make_response, jsonify
from flask.views import MethodView
from app.configurations import Config
from sqlalchemy import desc
from models.portfolio import Portfolio
from models.port_user_answers_set import PortUserAnswersSet
from api.utils import json_abort
from models.users import User


def create_result_as_dict(portfolios):
    result = list()
    for portfolio in portfolios:
        p_as_dict = portfolio.as_dict()
        del p_as_dict['risk']
        result.append(p_as_dict)
    return result


class RecentResults(MethodView):
    # get recent results
    def get(self):
        portfolios = Portfolio.query.order_by(desc(Portfolio.date_time)).limit(10).all()
        result = create_result_as_dict(portfolios)
        response = make_response(jsonify(result), 200)
        return response


class RecentResultsByUser(MethodView):
    # get recent results by user
    def get(self, user_id):
        portfolios = list()
        user = User.query.filter_by(_id=user_id).first()
        if user is None:
            json_abort(404, "Member not found")
        ports_user_ans = PortUserAnswersSet.query.filter_by(user_id=user_id).order_by(
            desc('portfolios_date_time')).limit(10).all()
        for port_user_ans in ports_user_ans:
            if port_user_ans.portfolio not in portfolios:
                portfolios.append(port_user_ans.portfolio)
            if len(portfolios) == 10:
                break
        result = create_result_as_dict(portfolios)
        response = make_response(jsonify(result), 200)
        return response


api = Blueprint('recent_results_api', __name__, url_prefix=Config.API_PREFIX + '/recent_results')
recent_results = RecentResults.as_view('api_recent_results')
recent_results_by_user = RecentResultsByUser.as_view('api_recent_results_by_user')
api.add_url_rule('/get_all', view_func=recent_results, methods=['GET'])
api.add_url_rule('/get_by_user/<string:user_id>', view_func=recent_results_by_user, methods=['GET'])
