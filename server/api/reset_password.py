from flask import Blueprint, request, make_response, jsonify, current_app
from flask.views import MethodView
from app.configurations import Config
from app.extensions import db
from api.utils import json_abort, exceptions_mapper, reset_pass_mail
from models.members import Member
from werkzeug.security import generate_password_hash, check_password_hash
from models.password_recovery import PasswordRecovery
import uuid


class RequestResetPassword(MethodView):
    def post(self):
        data = request.get_json()
        user_email = data.get("email")
        check_if_member_in_db = db.session.query(Member).filter_by(user_id=user_email).first()
        if not check_if_member_in_db:
            json_abort(409, "Member not found")
        uid = str(uuid.uuid4())
        password_recovery = PasswordRecovery(id=uid, member_email=user_email)
        db.session.add(password_recovery)
        db.session.commit()
        self.send_email(user_email, uid)
        response = make_response(jsonify(message="אימייל לשחזור סיסמה נשלח בהצלחה"), 200)
        return response

    def send_email(self, user_email, uid):
        reset_pass_mail(user_email, f'Reset password request, visit the following link: http://localhost:3000/reset_password/{uid}')


class EnterNewPassword(MethodView):
    def put(self):
        password_recovery = db.session.query(PasswordRecovery).filter_by(id=request.form['id']).first()
        if password_recovery is None:
            json_abort(404, "id not found")
        if password_recovery.is_used:
            json_abort(401, "Link has used")
        member = password_recovery.member
        new_password = request.form["new_password"]
        if new_password != request.form["new_password_again"]:
            json_abort(400, "Not the same password")
        new_password_encoded = generate_password_hash(new_password, method='sha256')
        member.password = new_password_encoded
        password_recovery.is_used = True
        db.session.commit()
        response = make_response(jsonify(message='הסיסמה עודכנה בהצלחה'), 200)
        return response


api = Blueprint('reset_password_api', __name__, url_prefix=Config.API_PREFIX + '/reset_password')
request_api = RequestResetPassword.as_view('request_api')
enter_new_password_api = EnterNewPassword.as_view('enter_new_password_api')
api.add_url_rule('/request', methods=['POST'], view_func=request_api)
api.add_url_rule('/set_new_password', methods=['PUT'], view_func=enter_new_password_api)
