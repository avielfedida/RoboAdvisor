from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from flask import Blueprint, request, make_response, jsonify, current_app
from api.utils import json_abort, get_tokens, token_required
from app.configurations import Config
from app.extensions import db
from models.members import Member
from werkzeug.security import generate_password_hash, check_password_hash
import jwt


class MembersApi(MethodView):
    # add new member
    def post(self):
        try:
            if request.form.get("latest_portfolio_risk"):
                new_member = Member(email=request.form['email'], password=request.form['password'],
                                    first_name=request.form['first_name'],
                                    last_name=request.form['last_name'], age=request.form['age'],
                                    gender=request.form['gender'],
                                    latest_portfolio_risk=request.form['latest_portfolio_risk'],
                                    user_id=request.form['user_id'])
            else:
                new_member = Member(email=request.form['email'], password=request.form['password'],
                                    first_name=request.form['first_name'],
                                    last_name=request.form['last_name'], age=request.form['age'],
                                    gender=request.form['gender'], user_id=request.form['user_id'])
            db.session.add(new_member)
            db.session.commit()
            response = make_response(jsonify(message="Member successfully added to database"), 200)

        except Exception as e:
            response = make_response(jsonify(message=str(e)), 400)

        return response

    # get member by email
    def get(self):
        try:
            member_by_email = db.session.query(Member).filter_by(email=request.args.get('email')).first()
            if member_by_email is None:
                response = make_response(jsonify(message='Invalid Member'), 400)
            else:
                response = make_response(jsonify(member_by_email.as_dict()), 200)
        except Exception as e:
            response = make_response(jsonify(message=str(e)), 400)

        return response


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
        # old_password_encoded = generate_password_hash(old_password, method='sha256')
        print("password in db: " + member.password)
        print(old_password)
        new_password = data.get("new_password")
        # new_password_encoded = generate_password_hash(new_password, method='sha256')
        print(new_password)
        # member_encode_password = generate_password_hash(member.password, method='sha256')
        if member.password == old_password:
        # if check_password_hash(member_encode_password, old_password_encoded):
        #     if not check_password_hash(member_encode_password, new_password_encoded):
            member.password = new_password
            db.session.commit()
            # new password is the same as the old password that in the db
            # else:
            #     json_abort(409, "This password already updated in this member")
        else:
            json_abort(401, "The password is incorrect")
        response = make_response(jsonify(message='Password updated successfully'), 200)
        return response


api = Blueprint('members_api', __name__, url_prefix=Config.API_PREFIX + '/members')
members = MembersApi.as_view('api_members')
member_login_api = MemberLogin.as_view('member_login_api')
member_update_name = MemberUpdateNames.as_view('member_update_name')
member_update_password = Member_update_password.as_view('member_update_password')
api.add_url_rule('/add_member/', methods=['POST'], view_func=members)
api.add_url_rule('/get_member_by_email/', methods=['GET'], view_func=members)
api.add_url_rule('/login', methods=['POST'], view_func=member_login_api)
api.add_url_rule('/update_name', methods=['PUT'], view_func=member_update_name)
api.add_url_rule('/update_password', methods=['PUT'], view_func=member_update_password)
