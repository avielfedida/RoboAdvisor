import unittest
from datetime import datetime

from tests.old_for_ref.test_base import TestBase
from tests.old_for_ref.utils import json_resp


class TradesTestCase(TestBase):

    def setUp(self):
        super(TradesTestCase, self).setUp()
        self.register_and_login()
        self.base += '/basic_info'

    def get_info(self):
        return self.client().get(self.base + '/',
                                 headers=self.headers)

    def test_get_info(self):
        res = self.get_info()
        self.assertEqual(200, res.status_code)
        assert all([x == 0 for x in json_resp(res).values()])
        # Insert study
        res = self.study_first_step("XAR", "15min time frame")
        self.assertEqual(200, res.status_code)
        token = json_resp(res).get('token')
        res = self.study_submit([], 'somescriptname', token)
        self.assertEqual(201, res.status_code)
        # Insert algorithm
        res = self.new_algorithm('sometitle')
        self.assertEqual(201, res.status_code)
        # Insert trade
        res = self.new_trade(50, 'sometitle', str(datetime.now()))
        self.assertEqual(201, res.status_code)
        res = self.get_info()
        self.assertEqual(200, res.status_code)
        assert all([x == 1 for x in json_resp(res).values()])


if __name__ == "__main__":
    unittest.main()
