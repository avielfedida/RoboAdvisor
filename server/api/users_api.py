from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError
from app.configurations import Config
from app.extensions import db
from models.users import User


class UsersApi(MethodView):

    # add new user
    def post(self):

        # TODO - Check if when not 'risk' is entered in the user table, is it set to undefined
        try:
            if request.form['latest_portfolio_risk']:
                new_user = User(email=request.form['email'], password=request.form['password'], first_name=request.form['first_name'],
                                last_name=request.form['last_name'], age=request.form['age'], sex=request.form['sex'],
                                latest_portfolio_risk=request.form['latest_portfolio_risk'])
            else:
                new_user = User(email=request.form['email'], password=request.form['password'], first_name=request.form['first_name'],
                                last_name=request.form['last_name'], age=request.form['age'], sex=request.form['sex'])
            db.session.add(new_user)
            db.session.commit()
            response = make_response(jsonify(message="User successfully added to database"), 200)

        except Exception as e:
            response = make_response(jsonify(message=str(e)), 400)

        return response

    # get user by email
    def get(self, email):

        try:
            user_by_email = db.session.query(User).filter_by(email=email).first()
            response = make_response(jsonify(user_by_email.as_dict()), 200)

        except AttributeError:
            response = make_response(jsonify(message="Something got wrong - You tried to get user by email"), 400)

        return response


api = Blueprint('users_api', __name__, url_prefix=Config.API_PREFIX + '/users')
users = UsersApi.as_view('api_users')
api.add_url_rule('/', methods=['POST'], view_func=users)
# api.add_url_rule('/get_user_by_email/<email>', methods=['GET'], view_func=users_api)
