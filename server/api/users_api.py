from flask.views import MethodView
from flask import Blueprint, request, make_response, jsonify
from app.configurations import Config
from app.extensions import db
from models.users import User

class UsersApi(MethodView):

    #add new user
     def post(self):
        try:
            new_user = User(_id=request.form['_id'])
            db.session.add(new_user)
            db.session.commit()
            response = make_response(jsonify(message="User successfully added to database"), 200)

        except Exception as e:
            response = make_response(jsonify(message=str(e)), 400)
        return response

     def put(self):
        try:
            user_by__id = db.session.query(User).filter_by(_id=request.args.get('_id')).first()
            if user_by__id is None:
                response = make_response(jsonify(message='Invalid User'), 400)
            else:
                user_by__id._id = request.form['email']
                db.session.commit()
                response = make_response(jsonify(message='User _id changed successfully'), 200)
        except Exception as e:
            response = make_response(jsonify(message=str(e)), 400)
        return response


api = Blueprint('users_api', __name__, url_prefix=Config.API_PREFIX + '/users')
users = UsersApi.as_view('api_users')
api.add_url_rule('/add_user/', methods=['POST'], view_func=users)
api.add_url_rule('/set_user_id/', methods=['PUT'], view_func=users)
