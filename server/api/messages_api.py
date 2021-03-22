from flask import Blueprint, request, make_response, jsonify, current_app
from flask.views import MethodView
from app.configurations import Config
from app.extensions import db
from models.topics import Topic
from models.members import Member
from models.messages import Message
from api.utils import token_required, json_abort


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


class SingleMessage(MethodView):
    def get(self, topic_id, msg_id):
        try:
            msg = db.session.query.filter_by(topic_id=topic_id, id=msg_id).first()
            if not msg:
                json_abort(404, "Message not found")
            response = make_response(jsonify(msg), 200)
            return response
        except Exception as e:
            json_abort(500, e)

    @token_required
    def put(self, curr_user):
        try:
            data = request.get_json()
            member = curr_user.member
            msg_id = data.get("id")
            topic_id = data.get("topic_id")
            msg = db.session.query.filter_by(eamil=member.email, topic_id=topic_id, id=msg_id).first()
            if not msg:
                json_abort(404, "Message not found")
            new_content = data.get("content")
            if not new_content:
                json_abort(400, "Content is empty")
            msg.content = new_content
            db.session.commit()
            response = make_response(jsonify(message='Message updated successfully'), 200)
            return response
        except Exception as e:
            json_abort(500, e)

    @token_required
    def post(self, curr_user):
        data = request.get_json()
        member = curr_user.member
        message_content = data.get("content")
        topic_id = data.get("topic_id")
        if not message_content or not topic_id:
            json_abort(400, "Content is empty")
        new_message = Message(content=message_content, member_email=member.email, topic_id=topic_id)
        if not new_message:
            json_abort(500, "Couldn't create new message")
        db.session.add(new_message)
        db.session.commit()
        response = make_response(jsonify(message='Message added successfully'), 200)
        return response


api = Blueprint('messages_api', __name__, url_prefix=Config.API_PREFIX + '/message')
single_message_get_api = SingleMessage.as_view('single_message_get_api')
single_message_api = SingleMessage.as_view('single_message_api')
api.add_url_rule('/get_single_message', methods=['GET'], view_func=single_message_get_api)
api.add_url_rule('/single_message', methods=['PUT', 'POST'], view_func=single_message_api)
