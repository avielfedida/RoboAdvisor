from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from app.configurations import Config
from app.extensions import db
from models.users import User


class UsersApi(MethodView):

    # add new user
    def post(self):
        try:
            if request.form.get("latest_portfolio_risk"):
                new_user = User(email=request.form['email'], password=request.form['password'], first_name=request.form['first_name'],
                                last_name=request.form['last_name'], age=request.form['age'], gender=request.form['gender'],
                                latest_portfolio_risk=request.form['latest_portfolio_risk'])
            else:
                new_user = User(email=request.form['email'], password=request.form['password'], first_name=request.form['first_name'],
                                last_name=request.form['last_name'], age=request.form['age'], gender=request.form['gender'])
            db.session.add(new_user)
            db.session.commit()
            response = make_response(jsonify(message="User successfully added to database"), 200)

        except Exception as e:
            response = make_response(jsonify(message=str(e)), 400)

        return response

    # get user by email
    def get(self):

        try:
            user_by_email = db.session.query(User).filter_by(email=request.args.get('email')).first()
            if user_by_email is None:
                response = make_response(jsonify(message='Invalid user'), 400)
            else:
                response = make_response(jsonify(user_by_email.as_dict()), 200)
        except Exception as e:
            response = make_response(jsonify(message=str(e)), 400)

        return response


api = Blueprint('users_api', __name__, url_prefix=Config.API_PREFIX + '/users')
users = UsersApi.as_view('api_users')
api.add_url_rule('/add_user/', methods=['POST'], view_func=users)
api.add_url_rule('/get_user_by_email/', methods=['GET'], view_func=users)
