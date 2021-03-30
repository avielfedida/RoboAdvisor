from flask import Blueprint, make_response, jsonify
from flask.views import MethodView
from app.configurations import Config
from algorithms.create_model import create_model
import json


class AlgorithmApi(MethodView):

    # add new stock price
    def get(self):
        try:
            algo = create_model('black_litterman', 5)
            portfolio = algo.build_portfolio()
            json_object = json.loads(portfolio)
            # lst = list(json_object['Weight'].values())
            # print(sorted([(x, i) for (i, x) in enumerate(lst)], reverse=True)[:3])
            response = make_response(json_object, 200)

        except Exception as e:
            response = make_response(jsonify(message=str(e)), 400)
        return response


api = Blueprint('algorithm_api', __name__, url_prefix=Config.API_PREFIX + '/algorithms')
algorithms = AlgorithmApi.as_view('api_algorithm')
api.add_url_rule('/black_litterman/', methods=['GET'], view_func=algorithms)
