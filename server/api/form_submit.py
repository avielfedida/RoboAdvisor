import json

from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

from api.algorithms import get_risk_horizon_score, check_if_all_questions_with_answers
from api.markowitz import Markowitz
from api.utils import exceptions_mapper, json_abort, plt_to_src
from app.configurations import Config
from app.extensions import db
from models.results import Results


class FormSubmit(MethodView):

    def get(self):
        new_result = Results(name='omer', notes=json.dumps({
            'hi': 3
        }))
        db.session.add(new_result)
        db.session.commit()
        return 'Ha'

    def post(self):
        try:
            dict_variable = {int(key) + 1: value+1 for (key, value) in request.json.items()}
            print('Answers', dict_variable)
        except Exception as e:
            json_abort(*exceptions_mapper(400, []), e)
        result = check_if_all_questions_with_answers(dict_variable)
        if result is not None:
            json_abort(*exceptions_mapper(400, result), e)
        else:
            for number_question in dict_variable.keys():
                answer_value = dict_variable[number_question]
                if number_question == 1:
                    # answer_value = dict_variable[number_question]
                    if not 1 <= answer_value <= 6:
                        json_abort(*exceptions_mapper(400, "Wrong range"))
                if number_question == 2:
                    # answer_value = dict_variable[number_question]
                    if not 1 <= answer_value <= 4:
                        json_abort(*exceptions_mapper(400, "Wrong range"))
                if number_question == 3:
                    # answer_value = dict_variable[number_question]
                    if not 1 <= answer_value <= 3:
                        json_abort(*exceptions_mapper(400, "Wrong range"))
                if number_question == 4:
                    # answer_value = dict_variable[number_question]
                    if not 1 <= answer_value <= 3:
                        json_abort(*exceptions_mapper(400, "Wrong range"))
                if number_question == 5:
                    # answer_value = dict_variable[number_question]
                    if not 1 <= answer_value <= 5:
                        json_abort(*exceptions_mapper(400, "Wrong range"))
                if number_question == 6:
                    # answer_value = dict_variable[number_question]
                    if not 1 <= answer_value <= 5:
                        json_abort(*exceptions_mapper(400, "Wrong range"))
                if number_question == 7:
                    # answer_value = dict_variable[number_question]
                    if not 1 <= answer_value <= 5:
                        json_abort(*exceptions_mapper(400, "Wrong range"))
                if number_question == 8:
                    # answer_value = dict_variable[number_question]
                    if not 1 <= answer_value <= 4:
                        json_abort(*exceptions_mapper(400, "Wrong range"))
        try:
            model = Markowitz()
            score = get_risk_horizon_score(dict_variable)
            fig = model.get_optimal_portfolio(0)
            base64image = plt_to_src(fig)
        except Exception as e:
            json_abort(*exceptions_mapper(500), e)
        return make_response(jsonify(message="Porfolio", src=base64image), 200)


api = Blueprint("api_form_submit", __name__, url_prefix=Config.API_PREFIX + '/form_submit')
form_submit = FormSubmit.as_view('form_submit_api')
api.add_url_rule('/', methods=['POST', 'GET'], view_func=form_submit)
