import datetime
import json

from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

from api.algorithms import get_risk_horizon_score, check_if_all_questions_with_answers
from api.markowitz import Markowitz
from api.utils import exceptions_mapper, json_abort, plt_to_src
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
            # Execute the model
            model = Markowitz()
            score = get_risk_horizon_score(dict_variable)
            if score is None:
                return make_response(jsonify(message="You have to accept a minimum risk."), 200)

            # Create the portfolio model # TODO: for now I did not use the risk Enum
            new_portfolio = Portfolio(algorithm=Algorithm.markowitz, risk=score, link="") # TODO: currently there is no link
            db.session.add(new_portfolio)


            # If there are not problems with the request we wish to add the different values
            uid = data.get('uid')

            # Create user if not existed
            if uid and len(uid) > 0:
                user = User.query.get(uid)
                if not user:
                    json_abort(*exceptions_mapper(400, "Invalid uid given"))
            else:
                uid = str(uuid.uuid4())
                user = User(uid)
                db.session.add(user)


            # Create answer set
            answers_array = [0] * len(answers)
            for k,v in answers.items():
                answers_array[int(k)] = v
            ans_set_val = ','.join(map(lambda x: str(x), answers_array))
            new_answers_set = AnswersSet.query.get(ans_set_val)
            if new_answers_set is None:
                new_answers_set = AnswersSet(ans_set_val=ans_set_val, ans_1=answers_array[0],
                                             ans_2=answers_array[1], ans_3=answers_array[2],
                                             ans_4=answers_array[3], ans_5=answers_array[4],
                                             ans_6=answers_array[5], ans_7=answers_array[6],
                                             ans_8=answers_array[7], risk=score)
                db.session.add(new_answers_set)

            db.session.commit()

            pua = PortUserAnswersSet(user_id=uid, ans_set_val=ans_set_val, portfolios_date_time=new_portfolio.date_time, portfolios_algorithm=new_portfolio.algorithm, portfolios_risk=score)
            db.session.add(pua)
            db.session.commit()

            json_res = model.get_optimal_portfolio(0)

            # TODO: here I should add to the PortfolioStocks model and set its primary key to the Portfolio
            # that was created

            # base64image = plt_to_src(fig)
        except Exception as e:
            json_abort(*exceptions_mapper(500), e)
        return make_response(jsonify(message="Porfolio", data=json_res), 200)


api = Blueprint("api_form_submit", __name__, url_prefix=Config.API_PREFIX + '/form_submit')
form_submit = FormSubmit.as_view('form_submit_api')
api.add_url_rule('/', methods=['POST', 'GET'], view_func=form_submit)
