from operator import itemgetter

from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

from api.algorithms import get_risk_horizon_score
from api.markowitz import model
from api.utils import exceptions_mapper, json_abort, plt_to_src

class FormSubmit(MethodView):
    def post(self):
        score = get_risk_horizon_score(request.json)
        fig = model.get_optimal_portfolio(score)
        base64image = plt_to_src(fig)
        #
        #
        # expected_fields = ['name']
        # try:
        #     name = itemgetter(*expected_fields)(request.form)
        # except Exception as e:
        #     json_abort(*exceptions_mapper(400, expected_fields), e)
        # try:
        #
        #     return make_response(jsonify(message="Algorithm added"), 201)
        # except Exception as e:
        #     json_abort(*exceptions_mapper(500), e)
        return make_response(jsonify(message="Porfolio", src=base64image), 200)


api = Blueprint("api_form_submit", __name__, url_prefix='/api/v1' + '/form_submit')
form_submit = FormSubmit.as_view('form_submit_api')
api.add_url_rule('/', methods=['POST'], view_func=form_submit)
