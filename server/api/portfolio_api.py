from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from app.configurations import Config
from app.extensions import db
from models.port_user_answers_set import PortUserAnswersSet
from models.portfolio import Portfolio
from datetime import datetime


class PortfolioApi(MethodView):

    # get portfolio by algorithm
    def get(self, link):
        try:
            portfolio_by_algorithm = db.session.query(Portfolio).filter_by(link=link).first()
            res = [ps.as_dict() for ps in portfolio_by_algorithm.portfolio_stocks]
            return make_response(jsonify(message="Porfolio", data=res), 200)
        except Exception as e:
            response = make_response(jsonify(message=str(e)), 400)

        return response


api = Blueprint('portfolio_api', __name__, url_prefix=Config.API_PREFIX + '/portfolios')
portfolios = PortfolioApi.as_view('api_portfolio')
api.add_url_rule('/add_portfolio/', methods=['POST'], view_func=portfolios)
api.add_url_rule('/get_portfolio_by_algorithm/<string:link>/', methods=['GET'], view_func=portfolios)
