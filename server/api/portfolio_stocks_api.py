from flask.views import MethodView
from flask import Blueprint, request, make_response, jsonify
from app.configurations import Config
from app.extensions import db
from models.portfolio_stocks import PortfolioStocks
from models.stock_price import StockPrice
from models.portfolio import Portfolio
from datetime import datetime


class PortfolioStocksApi(MethodView):

    # add port user answers set
     def post(self):
        try:

            date_time_str = request.form['date_time']
            date_time_obj = datetime.strptime(date_time_str, '%m-%d-%Y')

            stock_price = db.session.query(StockPrice).filter_by(date_time=date_time_obj, ticker=request.form['ticker']).first()

            portfolio = db.session.query(Portfolio).filter_by(date_time=date_time_obj, algorithm=request.form['algorithm'],
                                                              risk=request.form['risk']).first()

            new_portfolio_stocks = PortfolioStocks(stock_price=stock_price, portfolio=portfolio, weight=request.form['weight'])

            db.session.add(new_portfolio_stocks)
            db.session.commit()
            response = make_response(jsonify(message="StockPrice successfully added to database"), 200)

        except Exception as e:
            response = make_response(jsonify(message=str(e)), 400)
        return response


api = Blueprint('portfolio_stocks_api', __name__, url_prefix=Config.API_PREFIX + '/portfolio_stocks')
port_user_answers_set = PortfolioStocksApi.as_view('api_portfolio_stocks')
api.add_url_rule('/add_portfolio_stocks/', methods=['POST'], view_func=port_user_answers_set)
