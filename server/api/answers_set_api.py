from flask.views import MethodView
from flask import Blueprint, request, make_response, jsonify
from app.configurations import Config
from app.extensions import db
from models.answers_set import AnswersSet


class AnswersSetApi(MethodView):

    # add new answers_set
    def post(self):
        try:
            # new_answers_set = AnswersSet(ans_set_val=request.form['ans_set_val'], ans_1=request.form['ans_1'],
            #                              ans_2=request.form['ans_2'], ans_3=request.form['ans_3'],
            #                              ans_4=request.form['ans_4'], ans_5=request.form['ans_5'],
            #                              ans_6=request.form['ans_6'], ans_7=request.form['ans_7'],
            #                              ans_8=request.form['ans_8'])
            # db.session.add(new_answers_set)
            for risk in range(1, 5 + 1):
                for ans_1 in range(1, 6 + 1):
                    for ans_2 in range(1, 4 + 1):
                        for ans_3 in range(1, 3 + 1):
                            for ans_4 in range(1, 3 + 1):
                                for ans_5 in range(1, 5 + 1):
                                    for ans_6 in range(1, 5 + 1):
                                        for ans_7 in range(1, 5 + 1):
                                            for ans_8 in range(1, 4 + 1):
                                                # print(
                                                #     template.format("'{}_{}_{}_{}_{}_{}_{}_{}'".format(ans_1, ans_2, ans_3, ans_4, ans_5, ans_6, ans_7, ans_8),
                                                #                     ans_1, ans_2, ans_3, ans_4, ans_5, ans_6, ans_7, ans_8, risk)
                                                # )
                                                #
                                                new_answers_set = AnswersSet(
                                                    ans_set_val="{}_{}_{}_{}_{}_{}_{}_{}_{}".format(risk, ans_1, ans_2, ans_3,
                                                                                                 ans_4, ans_5, ans_6,
                                                                                                 ans_7, ans_8),
                                                    ans_1=str(ans_1),
                                                    ans_2=str(ans_2),
                                                    ans_3=str(ans_3),
                                                    ans_4=str(ans_4),
                                                    ans_5=str(ans_5),
                                                    ans_6=str(ans_6),
                                                    ans_7=str(ans_7),
                                                    ans_8=str(ans_8),
                                                    risk=risk)
                                                db.session.add(new_answers_set)
            db.session.commit()
            response = make_response(jsonify(message="Answers Set successfully added to database"), 200)

        except Exception as e:
            response = make_response(jsonify(message=str(e)), 400)
        return response


api = Blueprint('answers_sets_api', __name__, url_prefix=Config.API_PREFIX + '/answers_sets')
answers_sets = AnswersSetApi.as_view('api_answers_sets')
api.add_url_rule('/add_new_answers_set/', methods=['POST'], view_func=answers_sets)
