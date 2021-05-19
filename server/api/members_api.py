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
            json_abort(401, "שם משתמש/סיסמה לא נמצאו")
        return make_response(jsonify({'access_token': get_tokens(member.email, current_app), **member.as_dict()}), 200)


class MemberUpdateNames(MethodView):
    @token_required
    def put(self, curr_user):
        data = request.get_json()
        if curr_user is None:
            json_abort(401, "לא נמצא משתמש רשום עם פרטים אלו")
        member = curr_user.member
        new_first_name = data.get("first_name")
        new_last_name = data.get("last_name")

        if len(new_first_name) > 0:
            member.first_name = new_first_name

        if len(new_last_name) > 0:
            member.last_name = new_last_name

        db.session.add(member)
        db.session.commit()

        return make_response(jsonify(message='הפרופיל עודכן בהצלחה'), 200)


class Member_update_password(MethodView):
    @token_required
    def put(self, curr_user):
        data = request.get_json()
        if curr_user is None:
            json_abort(401, "לא נמצא משתמש רשום עם פרטים אלו")
        member = curr_user.member
        old_password = data.get("password")
        # old_password_encoded = generate_password_hash(old_password, method='sha256')
        new_password = data.get("new_password")
        if check_password_hash(member.password, old_password):
            if check_password_hash(member.password, new_password):
                json_abort(409, "זוהי כבר הסיסמה הנוכחית")
            else:
                new_password_encoded = generate_password_hash(new_password, method='sha256')
                member.password = new_password_encoded
                db.session.commit()
                response = make_response(jsonify(message='הסיסמה עודכנה בהצלחה'), 200)
                return response
        else:
            json_abort(401, "זו אינה הסיסמה הישנה")


api = Blueprint('members_api', __name__, url_prefix=Config.API_PREFIX + '/members')
member_login_api = MemberLogin.as_view('member_login_api')
member_update_name = MemberUpdateNames.as_view('member_update_name')
member_update_password = Member_update_password.as_view('member_update_password')
api.add_url_rule('/login', methods=['POST'], view_func=member_login_api)
api.add_url_rule('/update_name', methods=['PUT'], view_func=member_update_name)
api.add_url_rule('/update_password', methods=['PUT'], view_func=member_update_password)
