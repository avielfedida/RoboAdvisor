import datetime
import json

from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from sqlalchemy import desc

from api.algorithms import get_risk_horizon_score, check_if_all_questions_with_answers
from api.utils import exceptions_mapper, json_abort, plt_to_src, is_valid_model_name
from app.configurations import Config
from app.extensions import db
from models.answers_set import AnswersSet
from models.enums.algorithm import Algorithm
from models.port_user_answers_set import PortUserAnswersSet
from models.portfolio import Portfolio
from models.results import Results
from models.users import User
import uuid

class FormSubmit(MethodView):

    def post(self):
        data = request.get_json()
        model_name = data['model_name']
        if not is_valid_model_name(model_name):
            json_abort(*exceptions_mapper(400, 'שם המודל שהוזן אינו חוקי'))
        answers = data['answers']
        try:
            dict_variable = {int(key) + 1: value + 1 for (key, value) in answers.items()}
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
                        json_abort(*exceptions_mapper(400, "התשובה אינה בטווח התשובות האפשריות"))
                if number_question == 2:
                    # answer_value = dict_variable[number_question]
                    if not 1 <= answer_value <= 4:
                        json_abort(*exceptions_mapper(400, "התשובה אינה בטווח התשובות האפשריות"))
                if number_question == 3:
                    # answer_value = dict_variable[number_question]
                    if not 1 <= answer_value <= 3:
                        json_abort(*exceptions_mapper(400, "התשובה אינה בטווח התשובות האפשריות"))
                if number_question == 4:
                    # answer_value = dict_variable[number_question]
                    if not 1 <= answer_value <= 3:
                        json_abort(*exceptions_mapper(400, "התשובה אינה בטווח התשובות האפשריות"))
                if number_question == 5:
                    # answer_value = dict_variable[number_question]
                    if not 1 <= answer_value <= 5:
                        json_abort(*exceptions_mapper(400, "התשובה אינה בטווח התשובות האפשריות"))
                if number_question == 6:
                    # answer_value = dict_variable[number_question]
                    if not 1 <= answer_value <= 5:
                        json_abort(*exceptions_mapper(400, "התשובה אינה בטווח התשובות האפשריות"))
                if number_question == 7:
                    # answer_value = dict_variable[number_question]
                    if not 1 <= answer_value <= 5:
                        json_abort(*exceptions_mapper(400, "התשובה אינה בטווח התשובות האפשריות"))
                if number_question == 8:
                    # answer_value = dict_variable[number_question]
                    if not 1 <= answer_value <= 4:
                        json_abort(*exceptions_mapper(400, "התשובה אינה בטווח התשובות האפשריות"))

        try:
            score = get_risk_horizon_score(dict_variable)
            if score is None:
                return make_response(jsonify(message="קיבלת רמת סיכון מינימלית"), 200)

            # If there are not problems with the request we wish to add the different values
            uid = data.get('uid')

            # Create user if not existed
            if uid and len(uid) > 0:
                user = User.query.get(uid)
                if not user:
                    json_abort(*exceptions_mapper(400, "המזהה אינו חוקי"))
            else:
                uid = str(uuid.uuid4())
                user = User(_id=uid)
                db.session.add(user)

            # Get AnswersSet
            answer_set_pk = "{}_{}_{}_{}_{}_{}_{}_{}_{}".format(score, dict_variable[1], dict_variable[2], dict_variable[3],
                                                dict_variable[4], dict_variable[5], dict_variable[6],
                                                dict_variable[7], dict_variable[8])
            answers_set = AnswersSet.query.get(answer_set_pk)
            if not answers_set:
                json_abort(*exceptions_mapper(500, "לא נמצאו התשובות לשאלון"))

            # Get portfolio
            portfolio = Portfolio.query.filter_by(algorithm=model_name, risk=score).order_by(desc('date_time')).first()
            if not portfolio:
                json_abort(*exceptions_mapper(500, "תהליך מציאת תיק השקעות נכשל"))

            if not db.session.query(PortUserAnswersSet).filter_by(user_id=uid, ans_set_val=answer_set_pk,
                               portfolios_id=portfolio.id).first():
                pua = PortUserAnswersSet(user_id=uid, ans_set_val=answer_set_pk, portfolios_date_time=portfolio.date_time,
                                         portfolios_id=portfolio.id)
                db.session.add(pua)
                db.session.commit()
        except Exception as e:
            json_abort(*exceptions_mapper(500), e)
        return make_response(jsonify(message="Porfolio", link=portfolio.link), 200)


api = Blueprint("api_form_submit", __name__, url_prefix=Config.API_PREFIX + '/form_submit')
form_submit = FormSubmit.as_view('form_submit_api')
api.add_url_rule('/submit', methods=['POST', 'GET'], view_func=form_submit)
