from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from flask import Blueprint, request, make_response, jsonify, current_app
from api.utils import json_abort, get_tokens, token_required
from app.configurations import Config
from app.extensions import db
from models.members import Member
from werkzeug.security import generate_password_hash, check_password_hash
import jwt


class MemberLogin(MethodView):
    def post(self):
        data = request.get_json()
        member = Member.authenticate(**data)
        if not member:
            json_abort(401, "Incorrect username or password")
        return make_response(jsonify({'access_token': get_tokens(member.email, current_app)}), 200)


class MemberUpdateNames(MethodView):
    @token_required
    def put(self, curr_user):
        data = request.get_json()
        if curr_user is None:
            json_abort(404, "Member not found")
        member = curr_user.member
        new_first_name = data.get("first_name")
        new_last_name = data.get("last_name")
        if new_first_name and new_last_name:
            self.updateFirstName(member, new_first_name)
            self.updateLastName(member, new_last_name)
            response = make_response(jsonify(message='Names updated successfully'), 200)
            return response
        # only first name
        elif new_first_name and not new_last_name:
            self.updateFirstName(member, new_first_name)
            response = make_response(jsonify(message='First name updated successfully'), 200)
            return response
        # only last name
        elif new_last_name and not new_first_name:
            self.updateLastName(member, new_last_name)
            response = make_response(jsonify(message='Last name updated successfully'), 200)
            return response
        else:
            json_abort(400, "Missing fields please try again")

    def updateFirstName(self, member, new_first_name):
        old_name = member.first_name
        if old_name == new_first_name:
            json_abort(409, "This name already updated in this member")
        else:
            member.first_name = new_first_name
            db.session.commit()

    def updateLastName(self, member, new_last_name):
        old_name = member.last_name
        if old_name == new_last_name:
            json_abort(409, "This name already updated in this member")
        else:
            member.last_name = new_last_name
            db.session.commit()


class Member_update_password(MethodView):
    @token_required
    def put(self, curr_user):
        data = request.get_json()
        if curr_user is None:
            json_abort(404, "Member not found")
        member = curr_user.member
        old_password = data.get("password")
        print(old_password)
        # old_password_encoded = generate_password_hash(old_password, method='sha256')
        new_password = data.get("new_password")
        if check_password_hash(member.password, old_password):
            if check_password_hash(member.password, new_password):
                json_abort(409, "This password already updated in this member")
            else:
                new_password_encoded = generate_password_hash(new_password, method='sha256')
                member.password = new_password_encoded
                db.session.commit()
                response = make_response(jsonify(message='Password updated successfully'), 200)
                return response
        else:
            json_abort(401, "The password is incorrect")


api = Blueprint('members_api', __name__, url_prefix=Config.API_PREFIX + '/members')
member_login_api = MemberLogin.as_view('member_login_api')
member_update_name = MemberUpdateNames.as_view('member_update_name')
member_update_password = Member_update_password.as_view('member_update_password')
api.add_url_rule('/login', methods=['POST'], view_func=member_login_api)
api.add_url_rule('/update_name', methods=['PUT'], view_func=member_update_name)
api.add_url_rule('/update_password', methods=['PUT'], view_func=member_update_password)
