from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from app.configurations import Config
from app.extensions import db
from models.clusters import Cluster


class ClustersApi(MethodView):

    # add new cluster
    def post(self):
        try:
            new_cluster = Cluster(title=request.form['title'], description=request.form['description'])
            db.session.add(new_cluster)
            db.session.commit()
            response = make_response(jsonify(message="Cluster successfully added to database"), 200)

        except Exception as e:
            response = make_response(jsonify(message=str(e)), 400)

        return response


api = Blueprint('clusters_api', __name__, url_prefix=Config.API_PREFIX + '/cluster')
clusters = ClustersApi.as_view('api_clusters')
api.add_url_rule('/add_cluster/', methods=['POST'], view_func=clusters)
