from flask.views import MethodView
from flask import Blueprint, request, make_response, jsonify
from app.configurations import Config
from app.extensions import db
from models.port_user_answers_set import PortUserAnswersSet
from models.users import User
from models.portfolio import Portfolio
from models.answers_set import AnswersSet
from datetime import datetime


class PortUserAnswersSetApi(MethodView):

    # add port user answers set
     def post(self):
        try:
            user_by_id = db.session.query(User).filter_by(_id=request.form['user_id']).first()

            date_time_str = request.form['date_time']
            date_time_obj = datetime.strptime(date_time_str, '%m-%d-%Y')
            portfolio = db.session.query(Portfolio).filter_by(date_time=date_time_obj, algorithm=request.form['algorithm'],
                                                              risk=request.form['risk']).first()

            ans_set = db.session.query(AnswersSet).filter_by(ans_set_val=request.form['ans_set_val']).first()

            new_port_user_answers_set = PortUserAnswersSet(user_id=user_by_id, portfolios_id=portfolio.id, portfolios_date_time=portfolio.date_time, ans_set_val=ans_set)

            db.session.add(new_port_user_answers_set)
            db.session.commit()
            response = make_response(jsonify(message="PortUserAnswersSet successfully added to database"), 200)

        except Exception as e:
            response = make_response(jsonify(message=str(e)), 400)
        return response


api = Blueprint('port_user_answers_set_api', __name__, url_prefix=Config.API_PREFIX + '/port_user_answers_set')
port_user_answers_set = PortUserAnswersSetApi.as_view('api_port_user_answers_set')
api.add_url_rule('/add_port_user_answers_set/', methods=['POST'], view_func=port_user_answers_set)
