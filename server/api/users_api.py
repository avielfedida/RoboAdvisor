from flask import Blueprint, request, make_response, jsonify, current_app
from flask.views import MethodView
from app.configurations import Config
from app.extensions import db
from api.utils import json_abort, exceptions_mapper
import jwt
import hashlib
from datetime import datetime, timedelta
from models.users import User


def get_tokens(user_id, app):
    _access_token = jwt.encode({'uid': user_id,
                                'exp': datetime.utcnow() + timedelta(minutes=120),
                                'iat': datetime.utcnow()},
                               app.config['SECRET_KEY']).decode('utf-8')


class UsersApi(MethodView):

    # add new user
    def post(self):
        try:
            if request.form.get("latest_portfolio_risk"):
                new_user = User(email=request.form['email'], password=request.form['password'],
                                first_name=request.form['first_name'],
                                last_name=request.form['last_name'], age=request.form['age'],
                                gender=request.form['gender'],
                                latest_portfolio_risk=request.form['latest_portfolio_risk'])
            else:
                new_user = User(email=request.form['email'], password=request.form['password'],
                                first_name=request.form['first_name'],
                                last_name=request.form['last_name'], age=request.form['age'],
                                gender=request.form['gender'])
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


class UserLogin(MethodView):
    def post(self):
        data = request.get_json()
        user = User.authenticate(**data)
        if not user:
            json_abort(401, "Incorrect username or password")
        return make_response(jsonify({'access_token': get_tokens(user.email, current_app)}), 200)


class RegisterUser(MethodView):
    def post(self):
        data = request.get_json()
        user = User(**data)
        db.session.add(user)
        db.session.commit()
        return user.to_dict(), 201


api = Blueprint('users_api', __name__, url_prefix=Config.API_PREFIX + '/users')
users = UsersApi.as_view('api_users')
user_login_api = UserLogin.as_view('user_login_api')
user_register_api = RegisterUser.as_view('user_register_api')
api.add_url_rule('/add_user/', methods=['POST'], view_func=users)
api.add_url_rule('/get_user_by_email/', methods=['GET'], view_func=users)
api.add_url_rule('/login', methods=['POST'], view_func=user_login_api)
api.add_url_rule('/register', methods=['POST'], view_func=user_register_api)
