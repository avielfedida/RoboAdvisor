import unittest
from datetime import datetime
from tests.old_for_ref.test_base import TestBase
from tests.old_for_ref.utils import json_resp


class TradesTestCase(TestBase):

    def setUp(self):
        super(TradesTestCase, self).setUp()
        self.register_and_login()
        self.base += '/trades'


    def get_all_trades(self, page, perPage):
        return self.client().get(self.base + f'/{page}/{perPage}/',
                                 headers=self.headers)

    def get_trade(self, title):
        return self.client().get(self.base + f'/{title}',
                                 headers=self.headers)

    def get_trade_empty(self):
        return self.client().get(self.base + f'/',
                                 headers=self.headers)

    def update_trade(self, alg_name, added_date, data):
        return self.client().put(self.base + f'/{alg_name}/{added_date}',
                                   headers=self.headers, json=data)

    def delete_trade(self, alg_name, added_date):
        return self.client().delete(self.base + f'/{alg_name}/{added_date}',
                                    headers=self.headers)


    def test_new_trade(self):
        res = self.new_algorithm('sometitle')
        self.assertEqual(201, res.status_code)
        res = self.new_trade(50, 'sometitle', datetime.now())
        self.assertEqual(201, res.status_code)

    def test_get_all_trades(self):
        res = self.get_all_trades(1, 4)
        self.assertEqual(400, res.status_code)
        res = self.get_all_trades(0, 10)
        self.assertEqual(400, res.status_code)
        res = self.get_all_trades(-4, 10)
        self.assertEqual(404, res.status_code)
        res = self.get_all_trades(1, 10)
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, len(json_resp(res).get('datas')))
        res = self.get_all_trades(134141, 11414)
        self.assertEqual(500, res.status_code)
        res = self.new_algorithm('sometitle')
        self.assertEqual(201, res.status_code)
        res = self.new_trade(50, 'sometitle', str(datetime.now()))
        self.assertEqual(201, res.status_code)
        res = self.get_all_trades(1, 10)
        self.assertEqual(200, res.status_code)
        self.assertEqual(len(json_resp(res).get('datas')), 1)

    def test_update_trade(self):
        res = self.new_algorithm('another')
        self.assertEqual(201, res.status_code)
        res = self.new_algorithm('sometitle')
        self.assertEqual(201, res.status_code)
        dt = str(datetime.now())
        res = self.new_trade(50, 'sometitle', dt)
        self.assertEqual(res.status_code, 201)
        res = self.update_trade('sometitle', dt, {
            'pl': 30,
            'alg_name': 'another',
            'added_date': str(datetime.now())
        })
        self.assertEqual(204, res.status_code)
        res = self.update_trade('sometitle', dt, {
            'pl': 30,
            'alg_name': 'invalid_alg_name',
            'added_date': str(datetime.now())
        })
        self.assertEqual(404, res.status_code)

    def test_delete_trade(self):
        res = self.delete_trade('invalidname', datetime.now())
        self.assertEqual(404, res.status_code)
        res = self.new_algorithm('sometitle')
        self.assertEqual(201, res.status_code)
        # Still, the algorithm is good, but no trade with that datetime
        res = self.delete_trade('sometitle', datetime.now())
        self.assertEqual(404, res.status_code)
        dt = str(datetime.now())
        res = self.new_trade(50, 'sometitle', dt)
        self.assertEqual(201, res.status_code)
        res = self.delete_trade('sometitle', dt)
        self.assertEqual(204, res.status_code)

if __name__ == "__main__":
    unittest.main()
