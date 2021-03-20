from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from app.configurations import Config
from app.extensions import db
from models.topics import Topic
from models.members import Member
from models.messages import Message


class MessageApi(MethodView):

    # add new message
    def post(self):
        try:
            member = db.session.query(Member).filter_by(email=request.form['member_email']).first()
            topic = db.session.query(Topic).filter_by(id=request.form['topic_id']).first()
            new_message = Message(content=request.form['content'], topic=topic, member=member)
            db.session.add(new_message)
            db.session.commit()
            response = make_response(jsonify(message="Message successfully added to database"), 200)

        except Exception as e:
            response = make_response(jsonify(message=str(e)), 400)

        return response


api = Blueprint('messages_api', __name__, url_prefix=Config.API_PREFIX + '/message')
messages = MessageApi.as_view('api_topics')
api.add_url_rule('/add_message/', methods=['POST'], view_func=messages)
