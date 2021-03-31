import json
from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from app.configurations import Config


class StockPricesDataInsertApi(MethodView):

    def post(self):
        from celery_tasks.worker_tasks import insert_price_data
        # insert_price_data()
        insert_price_data.apply_async()  # args=[alg.as_dict(), analysis_type, params]) # No args for now
        return make_response(jsonify(message="OK"), 200)


api = Blueprint("stock_prices_data_insert", __name__, url_prefix=Config.API_PREFIX + '/stock_prices_data_insert')
stock_prices_data_insert = StockPricesDataInsertApi.as_view('api_stock_prices_data_insert')
api.add_url_rule('/', methods=['POST'], view_func=stock_prices_data_insert)
