from operator import itemgetter

from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

from api.algorithms import get_risk_horizon_score
from api.markowitz import Markowitz
from api.utils import exceptions_mapper, json_abort, plt_to_src

class FormSubmit(MethodView):
    def post(self):
        try:
            dict_variable = {int(key): value for (key, value) in request.json.items()}
        except Exception as e:
            json_abort(*exceptions_mapper(400, []), e)
        try:
            model = Markowitz()
            score = get_risk_horizon_score(dict_variable)
            print(score)
            fig = model.get_optimal_portfolio(score)
            base64image = plt_to_src(fig)
        except Exception as e:
            json_abort(*exceptions_mapper(500), e)
        return make_response(jsonify(message="Porfolio", src=base64image), 200)


api = Blueprint("api_form_submit", __name__, url_prefix='/api/v1' + '/form_submit')
form_submit = FormSubmit.as_view('form_submit_api')
api.add_url_rule('/', methods=['POST'], view_func=form_submit)
