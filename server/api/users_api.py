from flask import Blueprint, request, make_response, jsonify, current_app
from flask.views import MethodView
from app.configurations import Config
from app.extensions import db
from api.utils import json_abort, exceptions_mapper
import jwt
import hashlib
from datetime import datetime, timedelta
from models.users import User
from models.members import Member


def get_tokens(user_id, app):
    _access_token = jwt.encode({'uid': user_id,
                                'exp': datetime.utcnow() + timedelta(minutes=720),
                                'iat': datetime.utcnow()},
                               app.config['SECRET_KEY']).decode('utf-8')
    return _access_token


class UsersApi(MethodView):

    # add new user
    def post(self):
        try:
            new_user = User(_id=request.form['_id'])
            db.session.add(new_user)
            db.session.commit()
            response = make_response(jsonify(message="User successfully added to database"), 200)

        except Exception as e:
            response = make_response(jsonify(message=str(e)), 400)

        return response

    def put(self):
        try:
            user_by__id = db.session.query(User).filter_by(_id=request.args.get('_id')).first()
            if user_by__id is None:
                response = make_response(jsonify(message='Invalid User'), 400)
            else:
                user_by__id._id = request.form['email']
                db.session.commit()
                response = make_response(jsonify(message='User _id changed successfully'), 200)
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
        if data.get("_id") is None:
            self.createNewUser(data)
            self.createMember(data)
            response = make_response(jsonify(message="User successfully added to database"), 200)
        # the user submit the form at least one time
        else:
            user_id = data.get("_id")
            user_mail = data.get("email")
            user_from_db = db.session.query(User).filter_by(_id=user_id).first()
            user_from_db ._id = user_mail
            self.createMember(data)
            response = make_response(jsonify(message="User successfully added to database"), 200)
        return response

    def createMember(self, data):
        user_email = data.get("email")
        user_password = data.get("password")
        user_first_name = data.get("first_name")
        user_last_name = data.get("last_name")
        user_age = data.get("age")
        user_gender = data.get("gender")
        user_id = user_email
        new_member = Member(user_email, user_password, user_first_name, user_last_name, user_age, user_gender, user_id)
        db.session.add(new_member)
        db.session.commit()

    def createNewUser(self, data):
        user_email = data.get("email")
        new_user = User(user_email)
        db.session.add(new_user)
        db.session.commit()


api = Blueprint('users_api', __name__, url_prefix=Config.API_PREFIX + '/users')
# users = UsersApi.as_view('api_users')
user_login_api = UserLogin.as_view('user_login_api')
user_register_api = RegisterUser.as_view('user_register_api')
# api.add_url_rule('/add_user/', methods=['POST'], view_func=users)
# api.add_url_rule('/set_user_id/', methods=['PUT'], view_func=users)
api.add_url_rule('/login', methods=['POST'], view_func=user_login_api)
api.add_url_rule('/register', methods=['POST'], view_func=user_register_api)
