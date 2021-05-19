import json
from unittest import TestCase

import jwt

from app.configurations import Config
from app.extensions import db
from app.factory import create_app
from models.articles import Article

from tests.old_for_ref.utils import get_alg_report_file, get_study_in_sample_oos_files
from models.clusters import Cluster
'''
Regarding push/pop of contexts:
https://stackoverflow.com/questions/17375340/testing-code-that-requires-a-flask-app-or-request-context
'''


class TestBase(TestCase):
    #
    # @classmethod
    # def setUpClass(cls):
    #     print('Base class set up')
    #
    # @classmethod
    # def tearDownClass(cls):
    #     print('Base class tear down')

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.headers = {}
        # binds the app to the current context
        self.app_context = self.app.app_context()
        self.app_context.push()
        # create all tables
        # db.create_all()
        self.db = db
        self.prefix = Config.API_PREFIX
        self.base = self.prefix
        """Define test variables and initialize app."""

    def tearDown(self):
        # """teardown all initialized variables."""
        # drop all tables
        db.session.remove()
        # db.drop_all()
        self.app_context.pop()
        # self.app.app_context().pop()

    # def study_first_step(self, symbol, timeframe):
    #     cl = self.headers.copy()
    #     cl.update({
    #         "content_type": "multipart/form-data"
    #     })
    #     self.in_sample, self.oos = get_study_in_sample_oos_files()
    #     resp = self.client().post(f'{self.prefix}/studies/send_files', headers=cl, data={
    #         "symbol": symbol,
    #         'timeframe': timeframe,
    #         "in_sample": self.in_sample,
    #         "out_of_sample": self.oos
    #     })
    #     return resp

    # def study_submit(self, combinations, script_name, token):
    #     return self.client().post(f'{self.prefix}/studies/', headers=self.headers, json={
    #         'combinations': combinations,
    #         'script_name': script_name,
    #         'token': token
    #     })

    def register(self):
        username = 'loa4@gmail.com'
        password = 'pass4'
        first_name = 'first'
        last_name = 'last'
        birth_date = '2021/05/13'
        self.client().post(f'{self.prefix}/users/register', json=dict(email=username, password=password, first_name=first_name, last_name=last_name, date_of_birth=birth_date))

    def login(self, username, password):
        # username = 'patkennedy79@gmail.com'
        # password = 'FlaskIsAwesome'
        login_res = self.client().post(f'{self.prefix}/members/login', json=dict(email=username, password=password))
        self.access_token = json.loads(login_res.data)['access_token']
        token = jwt.decode(self.access_token, self.app.config['SECRET_KEY'], algorithms=["HS256"])
        self.user_id = token['uid']
        self.headers.update({'Authorization': f'Bearer {self.access_token}',
                             'Accept': "application/json"})

    def add_articles(self):
        self.db.session.add(
            Article(
                title='עמלות בבנקים וברוקרים פרטיים',
                description='במאמר זה נדון בעמלות השונות אותם גובים בנקים וברוקרים פרטיים',
                file='fees_in_the_banks_and_private_brokers.html'
            )
        )

        self.db.session.add(
            Article(
                title='מילון מונחים',
                description='בעמוד זה תוכלו למצוא מילון מונחים בסיסי עבור עולם הפיננסים',
                file='Glossary_of_Terms.html'
            )
        )

        self.db.session.add(
            Article(
                title='אלגוטרייד',
                description='במאמר זה נסביר על תחום האלגוטרייד',
                file='Algotrade_general.html'
            )
        )

        self.db.session.add(
            Article(
                title='ניהול השקעות עצמי',
                description='במאמר זה נציג מדריך לניהול השקעות עצמי',
                file='Guide_to_Independent_Investment_Management.html'
            )
        )

        self.db.session.add(
            Article(
                title='מודלים',
                description='במאמר זה נציג הסבר על המודלים השונים בהם אנו משתמשים באתר זה',
                file='Models.html'
            )
        )

        self.db.session.add(
            Article(
                title='יועצים רובוטים',
                description='במאמר זה נדון בתחום של יועצים רובוטיים, השירות העיקרי אותו האתר מספק',
                file='robo_advisor_general.html'
            )
        )
        self.db.session.commit()

    def add_clusters(self):
        self.db.session.add(
            Cluster(
                title='title1',
                description='במאמר זה נדון בעמלות השונות אותם גובים בנקים וברוקרים פרטיים',
                image_path='fees_in_the_banks_and_private_brokers.html'
            )
        )

        self.db.session.add(
            Cluster(
                title='title2',
                description='בעמוד זה תוכלו למצוא מילון מונחים בסיסי עבור עולם הפיננסים',
                image_path='Glossary_of_Terms.html'
            )
        )
        self.db.session.commit()
    # def new_algorithm(self, name):
    #     cl = self.headers.copy()
    #     cl.update({
    #         "content_type": "multipart/form-data"
    #     })
    #     my_file = get_alg_report_file()
    #     return self.client().post(f'{self.prefix}/algorithms/', headers=cl, data={
    #         "report_filename": my_file,
    #         'name': name,
    #     })

    # def get_algorithm(self, name):
    #     return self.client().get(f'{self.prefix}/algorithms/{name}',
    #                              headers=self.headers)
    #
    # def new_tech(self, title):
    #     return self.client().post(f'{self.prefix}/techniques/', headers=self.headers, json={
    #         'title': title,
    #         'description': 'another title'
    #     })

    # def new_trade(self, pl, alg_name, dt):
    #     return self.client().post(f'{self.prefix}/trades/', headers=self.headers, json={
    #         'pl': pl,
    #         'alg_name': alg_name,
    #         'added_date': dt
    #     })
