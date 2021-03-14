from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from flask import Blueprint, request, make_response, jsonify, current_app
from api.utils import json_abort
from app.configurations import Config
from app.extensions import db
from models.members import Member
import jwt
from datetime import datetime, timedelta


def get_tokens(user_id, app):
    _access_token = jwt.encode({'uid': user_id,
                                'exp': datetime.utcnow() + timedelta(minutes=720),
                                'iat': datetime.utcnow()},
                               app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')
    return _access_token


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


api = Blueprint('members_api', __name__, url_prefix=Config.API_PREFIX + '/members')
members = MembersApi.as_view('api_members')
member_login_api = MemberLogin.as_view('member_login_api')
api.add_url_rule('/add_member/', methods=['POST'], view_func=members)
api.add_url_rule('/get_member_by_email/', methods=['GET'], view_func=members)
api.add_url_rule('/login', methods=['POST'], view_func=member_login_api)
