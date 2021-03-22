from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from sqlalchemy import desc

from app.configurations import Config
from app.extensions import db
from models.topics import Topic
from models.members import Member
from models.clusters import Cluster
from api.utils import token_required, json_abort


class TopicsApi(MethodView):

    # add new topic
    def post(self):
        try:
            member = db.session.query(Member).filter_by(email=request.form['member_email']).first()
            cluster = db.session.query(Cluster).filter_by(title=request.form['cluster_title']).first()
            new_topic = Topic(title=request.form['title'], member=member, cluster=cluster)
            db.session.add(new_topic)
            db.session.commit()
            response = make_response(jsonify(message="Topic successfully added to database"), 200)

        except Exception as e:
            response = make_response(jsonify(message=str(e)), 400)

        return response


class SingleTopic(MethodView):
    @token_required
    def post(self, curr_user):
        data = request.get_json()
        member = curr_user.member
        topic_title = data.get("title")
        cluster_title = data.get("cluster_title")
        if not topic_title or not cluster_title:
            json_abort(400, "One or more of the titles is missing")
        new_topic = Topic(title=topic_title, member_email=member.email, cluster_title=cluster_title)
        if not new_topic:
            json_abort(500, "Couldn't create new topic")
        db.session.add(new_topic)
        db.session.commit()
        response = make_response(jsonify(message='Topic added successfully'), 200)
        return response

    def get(self, cluster_title):
        try:
            topic = db.session.query.filter_by(cluster_title=cluster_title).first()
            if not topic:
                json_abort(404, "Topic not found")
            response = make_response(jsonify(topic.as_dict()), 200)
            return response
        except Exception as e:
            json_abort(500, e)


class AllTopics(MethodView):
    def get(self, page, perPage, cluster_title):
        if page < 1 or perPage < 5:
            json_abort(400, "Missing on or more fields")
        try:
            all_topics = db.session.query.filter_by(cluster_title=cluster_title).order_by(desc('added_date')).paginate(
                page=page, perPage=perPage)
            response = make_response(jsonify(all_topics), 200)
            return response
        except Exception as e:
            json_abort(500, e)


api = Blueprint('topics_api', __name__, url_prefix=Config.API_PREFIX + '/topic')
single_topic_api = SingleTopic.as_view('single_topic_api')
api.add_url_rule('/single_topic', methods=['POST'], view_func=single_topic_api)
single_topic_get_api = SingleTopic.as_view('single_topic_get_api')
api.add_url_rule('/get_single_topic', methods=['GET'], view_func=single_topic_get_api)
topic_get_all_api = AllTopics.as_view('topic_get_all_api')
api.add_url_rule('/<int:page>/<int:perPage>/', methods=['GET'], view_func=topic_get_all_api)
