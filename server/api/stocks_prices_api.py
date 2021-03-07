from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from app.configurations import Config
from app.extensions import db
from models.stock_price import StockPrice
from datetime import datetime

class StocksPricesApi(MethodView):

    # add new stock price
    def post(self):
        try:
            date_time_str = request.form['date_time']
            date_time_obj = datetime.strptime(date_time_str, '%m-%d-%Y')
            new_stock_price = StockPrice(ticker=request.form['ticker'], date_time=date_time_obj, price=request.form['price'],
                                         asset_type=request.form['asset_type'])
            db.session.add(new_stock_price)
            db.session.commit()
            response = make_response(jsonify(message="Stock price successfully added to database"), 200)

        except Exception as e:
            response = make_response(jsonify(message=str(e)), 400)

        return response

    # get stock price by ticker
    def get(self):

        try:
            stock_price_by_email = db.session.query(StockPrice).filter_by(ticker=request.args.get('ticker')).first()
            if stock_price_by_email is None:
                response = make_response(jsonify(message='Invalid ticker'), 400)
            else:
                response = make_response(jsonify(stock_price_by_email.as_dict()), 200)
        except Exception as e:
            response = make_response(jsonify(message=str(e)), 400)

        return response


api = Blueprint('stocks_prices_api', __name__, url_prefix=Config.API_PREFIX + '/stocks_prices')
stocks_prices = StocksPricesApi.as_view('api_stocks_prices')
api.add_url_rule('/add_stock_price/', methods=['POST'], view_func=stocks_prices)
api.add_url_rule('/get_stock_price_by_ticker/', methods=['GET'], view_func=stocks_prices)
