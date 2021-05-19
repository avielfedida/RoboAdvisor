from tests.test_base import TestBase
import unittest


class PortfolioTest(TestBase):
    def setUp(self):
        super(PortfolioTest, self).setUp()
        self.base += '/portfolios'
        # self.username1 = 'aviel@gmail.com'
        # self.password1 = 'pass'

    def tearDown(self):
        super(PortfolioTest, self).tearDown()

    def test_get_portfolio_all_valid(self):
        res = self.client().get(f'{self.base}/get_portfolio_by_algorithm/e5798edc-4234-4e98-89f0-d4c4c657101c/'
                                , headers=self.headers)
        self.assertEqual(200, res.status_code)

    def test_get_portfolio_wrong_link(self):
        res = self.client().get(f'{self.base}/get_portfolio_by_algorithm/e5798edc-4234-4e98-89f0-d4c4c657101/'
                                , headers=self.headers)
        self.assertEqual(400, res.status_code)


if __name__ == "__main__":
    unittest.main()
