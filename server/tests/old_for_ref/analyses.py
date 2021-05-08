import unittest

from tests.old_for_ref.test_base import TestBase
from tests.old_for_ref.utils import json_resp


class TechniquesTestCase(TestBase):

    def setUp(self):
        super(TechniquesTestCase, self).setUp()
        self.register_and_login()
        self.base += '/analyses'

    def new_analyses(self, alg_name, analysis_type):
        return self.client().post(self.base + '/', headers=self.headers, json={
            'alg_name': alg_name,
            'analysis_type': analysis_type
        })

    def test_new_analyses(self):
        res = self.new_algorithm('sometitle')
        self.assertEqual(201, res.status_code)
        print(json_resp(res))
        res = self.new_analyses('sometitle', 'start_drawdown_analysis')
        self.assertEqual(res.status_code, 201)
        # task_id = json_resp(res)['task_id']
        # print(task_id)
        # interval = 3
        # limit = 5
        # state = None
        # for i in range(limit):
        #     time.sleep(interval)
        #     resp1 = get(self.base + '/{}'.format(task_id))
        #     state = resp1.json().get('state')
        # assert state == states.SUCCESS


if __name__ == "__main__":
    unittest.main()
