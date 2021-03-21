from flask import Blueprint, request, make_response, jsonify, current_app
from flask.views import MethodView
from app.configurations import Config
from app.extensions import db
from api.utils import json_abort, exceptions_mapper
import hashlib
from models.enums.gender import Gender
from models.users import User
from models.members import Member


class RegisterUser(MethodView):
    def post(self):
        data = request.get_json()
        print('Data: ', data)
        # first time in the system
        if data.get("_id") is None:
            user_email = data.get("email")
            check_if_member_in_db = db.session.query(Member).filter_by(user_id=user_email).first()
            if check_if_member_in_db:
                json_abort(409, "Member already exist")
            check_if_user_in_db = db.session.query(User).filter_by(_id=user_email).first()
            # if has user in db that its the email
            if check_if_user_in_db:
                self.createMember(data)
            # not exist in no db
            else:
                self.createNewUser(data)
                self.createMember(data)
            response = make_response(jsonify(message="User successfully added to database"), 200)
        # the user submit the form at least one time
        else:
            user_id = data.get("_id")
            user_mail = data.get("email")
            user_from_db = db.session.query(User).filter_by(_id=user_id).first()
            user_from_db._id = user_mail
            member_in_db = db.session.query(Member).filter_by(user_id=user_mail).first()
            if member_in_db is None:
                self.createMember(data)
                response = make_response(jsonify(message="User successfully added to database"), 200)
            else:
                json_abort(409, "Member already exist")

        return response

    def createMember(self, data):
        user_email = data.get("email")
        # check_if_in_member_db = db.session.query(Member).filter_by(user_id=user_email).first()
        # if check_if_in_member_db:
        #     json_abort(409, "Member already exist")
        user_password = data.get("password")
        user_first_name = data.get("first_name")
        user_last_name = data.get("last_name")
        user_age = 1  # data.get("age")
        user_gender = Gender.other  # data.get("gender")
        user_id = user_email
        if not user_email or not user_password or not user_first_name or not user_last_name or not user_age or not user_gender:
            json_abort(400, "Missing on or more fields")
        new_member = Member(user_email, user_password, user_first_name, user_last_name, user_age, user_gender, user_id)
        db.session.add(new_member)
        db.session.commit()

    def createNewUser(self, data):
        user_email = data.get("email")
        new_user = User(_id=user_email)
        db.session.add(new_user)
        db.session.commit()


api = Blueprint('users_api', __name__, url_prefix=Config.API_PREFIX + '/users')
user_register_api = RegisterUser.as_view('user_register_api')
api.add_url_rule('/register', methods=['POST'], view_func=user_register_api)
