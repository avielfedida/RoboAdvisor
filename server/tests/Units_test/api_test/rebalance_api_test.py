from tests.test_base import TestBase
import unittest


class RebalanceTest(TestBase):
    def setUp(self):
        super(RebalanceTest, self).setUp()
        self.base += '/rebalance'
        self.username1 = 'moran1@gmail.com'
        self.password1 = 'moran1'

    def tearDown(self):
        super(RebalanceTest, self).tearDown()

    def test_rebalance_all_valid(self):
        self.login(self.username1, self.password1)
        json = {
            "link": "fd393461-0869-4d72-b235-fbba61f0d0cc"}
        res = self.client().post(self.base + '/rebalanced', headers=self.headers, json=json)
        self.assertEqual(200, res.status_code)

    def test_rebalance_wrong_link(self):
        self.login(self.username1, self.password1)
        json = {
            "link": "e5798edc-4234-4e98-89f0-d4c4c657102c"}
        res = self.client().post(self.base + '/rebalanced', headers=self.headers, json=json)
        self.assertEqual(400, res.status_code)


if __name__ == "__main__":
    unittest.main()
