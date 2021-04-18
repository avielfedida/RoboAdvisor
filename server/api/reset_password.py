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
        stylesheet = '''
        body {
            text-align: right;
            direction: rtl;
        }
        '''
        # Note, links like: <a href="www.google.com">לינק איפוס</a>
        # will work really good and did not even considered as spam.
        reset_pass_mail(user_email, 'RoboAdvisor - איפוס סיסמא', f'''
        <html>
            <head>
            <style>
                {stylesheet}
            </style>
            </head>
            <body>
            <h1>איפוס סיסמא</h1>
            התקבלה בקשה לאיפוס סיסמתך, להמשך תהליך, נא להשתמש בלינק הבא: <a href="http://localhost:3000/reset_password/{uid}">לינק איפוס</a>
            <p>אם הלינק לא מופיע, אנא בצע העתקה אל חלון הכתובת בדפדפן של הכתובת</p>
            <p>http://localhost:3000/reset_password/{uid}</p>
            </body>
        </html>
        ''')
        response = make_response(jsonify(message="אימייל לשחזור סיסמה נשלח בהצלחה"), 200)
        return response

class EnterNewPassword(MethodView):
    def put(self):
        data = request.get_json()
        password_recovery = db.session.query(PasswordRecovery).filter_by(id=data.get('id')).first()
        if password_recovery is None:
            json_abort(404, "id not found")
        if password_recovery.is_used:
            json_abort(401, "Link has used")
        member = password_recovery.member
        new_password = data.get("new_password")
        member.password = generate_password_hash(new_password, method='sha256')
        password_recovery.is_used = True
        db.session.commit()
        response = make_response(jsonify(message='הסיסמה עודכנה בהצלחה'), 200)
        return response


api = Blueprint('reset_password_api', __name__, url_prefix=Config.API_PREFIX + '/reset_password')
request_api = RequestResetPassword.as_view('request_api')
enter_new_password_api = EnterNewPassword.as_view('enter_new_password_api')
api.add_url_rule('/request', methods=['POST'], view_func=request_api)
api.add_url_rule('/set_new_password', methods=['PUT'], view_func=enter_new_password_api)
