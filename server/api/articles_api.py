from flask import Blueprint, request, make_response, jsonify, send_from_directory, current_app
from flask.views import MethodView
from app.configurations import Config
from app.extensions import db
from models.articles import Article
from api.utils import json_abort
import os

from run import ROOT_DIR

class GetAllArticles(MethodView):
    def get(self):
        articles = db.session.query(Article).all()
        result = dict(articles=[c.as_dict() for c in articles])
        response = make_response(jsonify(result), 200)
        return response


class GetSingleArticle(MethodView):
    def get(self, article_id):
        article = Article.query.get(article_id)
        if not article:
            json_abort(404, "המאמר לא נמצא")
        return send_from_directory(filename=article.file, directory=os.path.join(os.path.join(os.getcwd(), 'api'), 'articles'))
        # return send_from_directory(filename=article.file, directory=os.path.join(os.path.join(ROOT_DIR, 'api'), 'articles'))


api = Blueprint('articles_api', __name__, url_prefix=Config.API_PREFIX + '/articles')
articles_api = GetAllArticles.as_view('articles_api')
article_api = GetSingleArticle.as_view('article_api')
api.add_url_rule('/get_articles', methods=['GET'], view_func=articles_api)
api.add_url_rule('/get_article/<int:article_id>', methods=['GET'], view_func=article_api)
