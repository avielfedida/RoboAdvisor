import json
from unittest import TestCase

import jwt

from app.configurations import Config
from app.extensions import db
from app.factory import create_app
from tests.old_for_ref.utils import get_alg_report_file, get_study_in_sample_oos_files

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
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.headers = {}
        # binds the app to the current context
        self.app.app_context().push()
        # create all tables
        db.create_all()
        self.db = db
        self.prefix = Config.API_PREFIX
        self.base = self.prefix
        """Define test variables and initialize app."""

    def tearDown(self):
        # """teardown all initialized variables."""
        # drop all tables
        db.session.remove()
        db.drop_all()
        self.app.app_context().pop()

    # TODO: ResourceWarning: unclosed file <_io.BufferedRandom name=5> return self.open(*args, **kw)
    def study_first_step(self, symbol, timeframe):
        cl = self.headers.copy()
        cl.update({
            "content_type": "multipart/form-data"
        })
        self.in_sample, self.oos = get_study_in_sample_oos_files()
        resp = self.client().post(f'{self.prefix}/studies/send_files', headers=cl, data={
            "symbol": symbol,
            'timeframe': timeframe,
            "in_sample": self.in_sample,
            "out_of_sample": self.oos
        })
        return resp

    def study_submit(self, combinations, script_name, token):
        return self.client().post(f'{self.prefix}/studies/', headers=self.headers, json={
            'combinations': combinations,
            'script_name': script_name,
            'token': token
        })

    def register_and_login(self):
        username = 'patkennedy79@gmail.com'
        password = 'FlaskIsAwesome'
        self.client().post(f'{self.prefix}/users/register',
                       json=dict(email=username, password=password))
        login_res = self.client().post(f'{self.prefix}/users/login', json=dict(email=username, password=password))
        self.access_token = json.loads(login_res.data)['access_token']
        token = jwt.decode(self.access_token, self.app.config['SECRET_KEY'], algorithms=["HS256"])
        self.user_id = token['uid']
        self.headers.update({'Authorization': f'Bearer {self.access_token}',
                             'Accept': "application/json"})

    def new_algorithm(self, name):
        cl = self.headers.copy()
        cl.update({
            "content_type": "multipart/form-data"
        })
        my_file = get_alg_report_file()
        return self.client().post(f'{self.prefix}/algorithms/', headers=cl, data={
            "report_filename": my_file,
            'name': name,
        })

    def get_algorithm(self, name):
        return self.client().get(f'{self.prefix}/algorithms/{name}',
                                 headers=self.headers)


    def new_tech(self, title):
        return self.client().post(f'{self.prefix}/techniques/', headers=self.headers, json={
            'title': title,
            'description': 'another title'
        })

    def new_trade(self, pl, alg_name, dt):
        return self.client().post(f'{self.prefix}/trades/', headers=self.headers, json={
            'pl': pl,
            'alg_name': alg_name,
            'added_date': dt
        })


