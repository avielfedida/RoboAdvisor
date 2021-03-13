from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from app.configurations import Config
from app.extensions import db
from models.members import Member


class MembersApi(MethodView):

    # add new member
    def post(self):
        try:
            if request.form.get("latest_portfolio_risk"):
                new_member = Member(email=request.form['email'], password=request.form['password'], first_name=request.form['first_name'],
                                    last_name=request.form['last_name'], age=request.form['age'], gender=request.form['gender'],
                                    latest_portfolio_risk=request.form['latest_portfolio_risk'], user_id =request.form['user_id'])
            else:
                new_member = Member(email=request.form['email'], password=request.form['password'], first_name=request.form['first_name'],
                                last_name=request.form['last_name'], age=request.form['age'], gender=request.form['gender'], user_id =request.form['user_id'])
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


api = Blueprint('members_api', __name__, url_prefix=Config.API_PREFIX + '/members')
members = MembersApi.as_view('api_members')
api.add_url_rule('/add_member/', methods=['POST'], view_func=members)
api.add_url_rule('/get_member_by_email/', methods=['GET'], view_func=members)
