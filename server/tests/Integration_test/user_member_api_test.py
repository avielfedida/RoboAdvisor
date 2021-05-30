import unittest
from tests.test_base import TestBase
import jwt
import json
import logging
import uuid


class UserMembersCase(TestBase):
    def setUp(self):
        super(UserMembersCase, self).setUp()
        self.username1 = 'moran4@gmail.com'
        self.password1 = 'moran4'

    def test_register_login(self):
        first_name = 'first'
        last_name = 'last'
        birth_date = '2021/05/13'
        res_register= self.client().post(f'{self.prefix}/users/register', json=dict(email=self.username1, password=self.password1,
                                                                      first_name=first_name, last_name=last_name,
                                                                      date_of_birth=birth_date))
        self.assertEqual(200, res_register.status_code)

        login_res = self.client().post(f'{self.prefix}/members/login', json=dict(email=self.username1, password=self.password1))
        self.access_token = json.loads(login_res.data)['access_token']
        token = jwt.decode(self.access_token, self.app.config['SECRET_KEY'], algorithms=["HS256"])
        self.user_id = token['uid']
        self.headers.update({'Authorization': f'Bearer {self.access_token}',
                             'Accept': "application/json"})

        self.assertEqual(200, login_res.status_code)


    def test_login_reset_password_by_email(self):
        password2 = 'm1234'
        login_res = self.client().post(f'{self.prefix}/members/login', json=dict(email=self.username1, password=password2))
        self.assertEqual(401, login_res.status_code)

        json = {'email': self.username1}
        res = self.client().post(f'{self.prefix}/reset_password/request', headers=self.headers, json=json)
        self.assertEqual(res.status_code, 200)

    def test_login_form_submit(self):
        login_res = self.client().post(f'{self.prefix}/members/login', json=dict(email=self.username1, password=self.password1))

        self.access_token = json.loads(login_res.data)['access_token']

        token = jwt.decode(self.access_token, self.app.config['SECRET_KEY'], algorithms=["HS256"])
        self.user_id = token['uid']
        self.headers.update({'Authorization': f'Bearer {self.access_token}',
                             'Accept': "application/json"})

        self.assertEqual(200, login_res.status_code)

        base = self.prefix+'/form_submit'
        model_name = 'markowitz'
        answers = {0: 2,
                        1: 2,
                        2: 2,
                        3: 2,
                        4: 2,
                        5: 2,
                        6: 2,
                        7: 2,
                        }
        json_ob = {
            'model_name': model_name,
            'answers': answers,
            'uid': self.user_id
        }
        res_form_submit = self.client().post(base + '/submit', headers=self.headers, json=json_ob)
        self.assertEqual(res_form_submit.status_code, 200)

    def test_login_form_submit_risk_resulting_is_minimal(self):
        login_res = self.client().post(f'{self.prefix}/members/login', json=dict(email=self.username1, password=self.password1))

        self.access_token = json.loads(login_res.data)['access_token']

        token = jwt.decode(self.access_token, self.app.config['SECRET_KEY'], algorithms=["HS256"])
        self.user_id = token['uid']
        self.headers.update({'Authorization': f'Bearer {self.access_token}',
                             'Accept': "application/json"})

        self.assertEqual(200, login_res.status_code)
        base = self.prefix + '/form_submit'
        model_name = 'markowitz'
        answers = {0: 0,
                   1: 2,
                   2: 2,
                   3: 2,
                   4: 2,
                   5: 2,
                   6: 2,
                   7: 2,
                   }
        json_ob = {
            'model_name': model_name,
            'answers': answers,
            'uid':  self.user_id
        }
        res_form_submit = self.client().post(base + '/submit', headers=self.headers, json=json_ob)
        self.assertEqual(res_form_submit.status_code, 200)

    def test_not_login_form_submit_risk_resulting_is_minimal(self):
        base = self.prefix +'/topics'
        json_obj = {
            "title": str(uuid.uuid4()),
            "cluster_title": "title1",
            "message": "bla"
        }
        res = self.client().post(base + '/single_topic', headers=self.headers, json=json_obj)
        self.assertEqual(401, res.status_code)

    def test_login_recent_results_get_by_user(self):
        login_res = self.client().post(f'{self.prefix}/members/login', json=dict(email=self.username1, password=self.password1))

        self.access_token = json.loads(login_res.data)['access_token']

        token = jwt.decode(self.access_token, self.app.config['SECRET_KEY'], algorithms=["HS256"])
        self.user_id = token['uid']
        self.headers.update({'Authorization': f'Bearer {self.access_token}',
                             'Accept': "application/json"})
        self.assertEqual(200, login_res.status_code)

        user_id = self.username1
        base = self.prefix+'/recent_results'
        res = self.client().get(base + '/get_by_user' + f'/{user_id}', headers=self.headers)
        self.assertEqual(res.status_code, 200)


    def test_login_rebalance_all_valid(self):
        login_res = self.client().post(f'{self.prefix}/members/login', json=dict(email=self.username1, password=self.password1))

        self.access_token = json.loads(login_res.data)['access_token']

        token = jwt.decode(self.access_token, self.app.config['SECRET_KEY'], algorithms=["HS256"])
        self.user_id = token['uid']
        self.headers.update({'Authorization': f'Bearer {self.access_token}',
                             'Accept': "application/json"})
        self.assertEqual(200, login_res.status_code)

        base = self.prefix+'/recent_results'
        res = self.client().get(base + '/get_by_user' + f'/{self.user_id}', headers=self.headers)
        link = json.loads(res.data.decode("utf-8"))[0]['link']
        self.assertEqual(res.status_code, 200)

        json_obj = {
            "link": link
        }

        base = self.prefix + '/rebalance'
        res = self.client().post(base + '/rebalanced', headers=self.headers, json=json_obj)
        self.assertEqual(200, res.status_code)

    def test_login_get_get_portfolio_wrong_link(self):
            login_res = self.client().post(f'{self.prefix}/members/login', json=dict(email=self.username1, password=self.password1))

            self.access_token = json.loads(login_res.data)['access_token']

            token = jwt.decode(self.access_token, self.app.config['SECRET_KEY'], algorithms=["HS256"])
            self.user_id = token['uid']
            self.headers.update({'Authorization': f'Bearer {self.access_token}',
                                 'Accept': "application/json"})
            self.assertEqual(200, login_res.status_code)

            json_obj = {
                "link": '12343fvfdbnthfbvfcd'
            }

            base = self.prefix + '/rebalance'
            res = self.client().post(base + '/rebalanced', headers=self.headers, json=json_obj)
            self.assertEqual(400, res.status_code)


if __name__ == "__main__":
    logging.disable(logging.CRITICAL)
    unittest.main()
