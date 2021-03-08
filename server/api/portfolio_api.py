from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from app.configurations import Config
from app.extensions import db
from models.portfolio import Portfolio
from datetime import datetime


class PortfolioApi(MethodView):

    # add new stock price
    def post(self):
        try:
            date_time_str = request.form['date_time']
            date_time_obj = datetime.strptime(date_time_str, '%m-%d-%Y')
            new_portfolio = Portfolio(date_time=date_time_obj, algorithm=request.form['algorithm'],
                                      risk=request.form['risk'], link=request.form['link'])
            db.session.add(new_portfolio)
            db.session.commit()
            response = make_response(jsonify(message="Portfolio added to database"), 200)

        except Exception as e:
            response = make_response(jsonify(message=str(e)), 400)

        return response

    # get portfolio by algorithm
    def get(self):

        try:
            portfolio_by_algorithm = db.session.query(Portfolio).filter_by(algorithm=request.args.get('algorithm')).first()
            response = make_response(jsonify(portfolio_by_algorithm.as_dict()), 200)
        except Exception as e:
            response = make_response(jsonify(message=str(e)), 400)

        return response


api = Blueprint('portfolio_api', __name__, url_prefix=Config.API_PREFIX + '/portfolios')
portfolios = PortfolioApi.as_view('api_portfolio')
api.add_url_rule('/add_portfolio/', methods=['POST'], view_func=portfolios)
api.add_url_rule('/get_portfolio_by_algorithm/', methods=['GET'], view_func=portfolios)