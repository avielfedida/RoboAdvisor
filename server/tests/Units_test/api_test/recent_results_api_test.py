import unittest
from tests.test_base import TestBase
import logging


class RecentResultsTestCase(TestBase):
    def setUp(self):
        super(RecentResultsTestCase, self).setUp()
        self.base += '/recent_results'

    def test_recent_results_get_all(self):
        res = self.client().get(self.base + '/get_all', headers=self.headers)
        self.assertEqual(res.status_code, 200)

    def test_recent_results_get_by_user(self):
        user_id = "aa6f0261-f604-42e3-be48-4c01d07193ed"
        res = self.client().get(self.base + '/get_by_user' + f'/{user_id}', headers=self.headers)
        self.assertEqual(res.status_code, 200)

    def test_recent_results_get_by_user_user_does_not_exist(self):
        user_id = "0"
        res = self.client().get(self.base + '/get_by_user' + f'/{user_id}', headers=self.headers)
        self.assertEqual(res.status_code, 404)


if __name__ == "__main__":
    logging.disable(logging.CRITICAL)
    unittest.main()