from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from app.configurations import Config
from app.extensions import db
from models.topics import Topic
from models.members import Member
from models.clusters import Cluster


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


api = Blueprint('topics_api', __name__, url_prefix=Config.API_PREFIX + '/topic')
topics = TopicsApi.as_view('api_topics')
api.add_url_rule('/add_topic/', methods=['POST'], view_func=topics)
