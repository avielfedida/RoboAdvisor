from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from app.configurations import Config
from algorithms.create_model import create_model



class AlgorithmApi(MethodView):

    # add new stock price
    def get(self):
        try:
            model_name = request.args.get('model_name')
            risk = int(request.args.get('risk'))
            algo = create_model(model_name, risk)
            portfolio = algo.get_portfolio_object()
            json_object = {'portfolio': portfolio.as_dict()}
            print(json_object)
            response = make_response(jsonify(message="האלגוריתם סיים לרוץ בהצלחה"), 200)

        except Exception as e:
            response = make_response(jsonify(message=str(e)), 400)
        return response


api = Blueprint('algorithm_api', __name__, url_prefix=Config.API_PREFIX + '/algorithms')
algorithms = AlgorithmApi.as_view('api_algorithm')
api.add_url_rule('/run_algorithm_by_name/', methods=['GET'], view_func=algorithms)
