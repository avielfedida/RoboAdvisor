from flask import Blueprint, request, make_response, jsonify, current_app
from flask.views import MethodView
from app.configurations import Config
from app.extensions import db
from api.utils import json_abort, exceptions_mapper
from models.members import Member
import uuid


class RequestResetPassword(MethodView):
    def post(self):
        data = request.get_json()
        user_email = data.get("email")
        check_if_member_in_db = db.session.query(Member).filter_by(user_id=user_email).first()
        if not check_if_member_in_db:
            json_abort(409, "Member not found")
        uid = str(uuid.uuid4())
        self.send_email(user_email, uid)
        response = make_response(jsonify(message="User successfully added to database"), 200)
        return response

    def send_email(self, user_email, uid):
        print("need to send the mail")


# class EnterNewPassword(MethodView):
#     def post(self):
#         data = request.get_json()


api = Blueprint('reset_password_api', __name__, url_prefix=Config.API_PREFIX + '/reset_password')
request_api = RequestResetPassword.as_view('request_api')
# enter_new_password_api = EnterNewPassword.as_view('enter_new_password_api')
api.add_url_rule('/request', methods=['POST'], view_func=request_api)
# api.add_url_rule('/new_password', methods=['POST'], view_func=enter_new_password_api)
