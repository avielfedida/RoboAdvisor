from flask import Blueprint, request, make_response, jsonify, current_app
from flask.views import MethodView
from sqlalchemy import desc, asc

from app.configurations import Config
from app.extensions import db
from models.topics import Topic
from models.members import Member
from models.messages import Message
from api.utils import token_required, json_abort


class SingleMessage(MethodView):
    def get(self, topic_id, msg_id):
        msg = db.session.query(Message).filter_by(topic_id=topic_id, id=msg_id).first()
        if not msg:
            json_abort(404, "ההודעה לא נמצאה")
        else:
            response = make_response(jsonify(msg.as_dict()), 200)
            return response

    @token_required
    def put(self, curr_user):
        data = request.get_json()
        member = curr_user.member
        msg_id = data.get("id")
        topic_id = data.get("topic_id")
        msg = db.session.query(Message).filter_by(member_email=member.email, topic_id=topic_id, id=msg_id).first()
        if not msg:
            json_abort(404, "ההודעה לא נמצאה")
        new_content = data.get("content")
        if not new_content:
            json_abort(400, "תוכן ההודעה ריק")
        msg.content = new_content
        db.session.commit()
        response = make_response(jsonify(message='ההודעה עודכנה בהצלחה'), 200)
        return response

    @token_required
    def post(self, curr_user):
        data = request.get_json()
        member = curr_user.member
        message_content = data.get("content")
        topic_id = data.get("topic_id")
        if not message_content or not topic_id:
            json_abort(400, "תוכן ההודעה ריק")
        new_message = Message(content=message_content, member_email=member.email, topic_id=topic_id)
        if not new_message:
            json_abort(500, "יצירת הודעה חדשה לא הצליחה")
        db.session.add(new_message)
        db.session.commit()
        response = make_response(jsonify(message='ההודעה התווספה בהצלחה'), 200)
        return response


class AllMessages(MethodView):
    def get(self, topic_id, page):
        if page < 1:
            json_abort(400, "כמות הדפים שהוכנסו לא חוקי")
        all_messages = Message.query.filter_by(topic_id=topic_id).order_by(asc('created_at')).paginate(
            page=page, per_page=Config.MESSAGES_PER_PAGE)
        result = dict(datas=[a.as_dict() for a in all_messages.items],
                      total=all_messages.total,
                      current_page=all_messages.page,
                      per_page=all_messages.per_page)
        response = make_response(jsonify(result), 200)
        return response


api = Blueprint('messages_api', __name__, url_prefix=Config.API_PREFIX + '/messages')
single_message_get_api = SingleMessage.as_view('single_message_get_api')
single_message_api = SingleMessage.as_view('single_message_api')
api.add_url_rule('/single/<int:topic_id>/<int:msg_id>', methods=['GET'], view_func=single_message_get_api)
api.add_url_rule('/single_message', methods=['PUT', 'POST'], view_func=single_message_api)
message_get_all_api = AllMessages.as_view('message_get_all_api')
api.add_url_rule('/all/<int:topic_id>/<int:page>', methods=['GET'], view_func=message_get_all_api)
