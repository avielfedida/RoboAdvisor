from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from app.configurations import Config
from app.extensions import db
from models.members import Member
from models.password_recovery import PasswordRecovery
from models.users import User


class PasswordRecoveryApi(MethodView):

    # add password recovery
    def post(self):
        try:
            email = request.form['email']
            date_time_str = request.form['date_of_birth']
            new_user = User(_id=email)
            db.session.add(new_user)
            db.session.commit()
            new_member = Member(email=email, password=request.form['password'], first_name=request.form['first_name'], last_name=request.form['last_name'] , date_of_birth = date_time_str, user_id=email)
            db.session.add(new_member)
            id = request.form['id']
            password_recovery = PasswordRecovery(id=id, member_email= email)
            db.session.add(password_recovery)
            db.session.commit()
            response = make_response(jsonify(message="add password recovery"), 200)

        except Exception as e:
            response = make_response(jsonify(message=str(e)), 400)
        return response


api = Blueprint('passwordRecoveryApi_api', __name__, url_prefix=Config.API_PREFIX + '/password_recovery')
password_recovery = PasswordRecoveryApi.as_view('api_password_recovery')
api.add_url_rule('/add_password_recovery/', methods=['POST'], view_func=password_recovery)