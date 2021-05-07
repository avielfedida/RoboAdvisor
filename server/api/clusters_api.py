from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from app.configurations import Config
from app.extensions import db
from models.clusters import Cluster
from api.utils import json_abort


class GetAllClusters(MethodView):
    def get(self):
        clusters = db.session.query(Cluster).all()
        result = dict(clusters=[c.as_dict() for c in clusters])
        response = make_response(jsonify(result), 200)
        return response


api = Blueprint('clusters_api', __name__, url_prefix=Config.API_PREFIX + '/cluster')
clusters_api = GetAllClusters.as_view('clusters_api')
api.add_url_rule('/get_clusters', methods=['GET'], view_func=clusters_api)
