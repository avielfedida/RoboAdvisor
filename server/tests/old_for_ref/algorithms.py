import unittest
from datetime import datetime

from tests.old_for_ref.test_base import TestBase
from tests.old_for_ref.utils import get_alg_report_file, json_resp


class AlgorithmsTestCase(TestBase):

    def setUp(self):
        super(AlgorithmsTestCase, self).setUp()
        self.register_and_login()
        self.base += '/algorithms'

    def new_algorithm_missing_name(self):
        cl = self.headers.copy()
        cl.update({
            "content_type": "multipart/form-data"
        })
        my_file = get_alg_report_file()
        return self.client().post(self.base + '/', headers=cl, data={
            "report_filename": my_file,
        })

    def new_algorithm_missing_file(self, name):
        cl = self.headers.copy()
        cl.update({
            "content_type": "multipart/form-data"
        })
        return self.client().post(self.base + '/', headers=cl, data={
            "name": name,
        })

    def get_all_algorithms(self, page, perPage):
        return self.client().get(self.base + f'/{page}/{perPage}/',
                                 headers=self.headers)


    def get_algorithm_empty(self):
        return self.client().get(self.base + f'/',
                                 headers=self.headers)

    def update_algorithm(self, name, new_oosbdate):
        return self.client().patch(self.base + f'/{name}',
                                   headers=self.headers, json={
                'oos_bdate': new_oosbdate
            })

    def delete_algorithm(self, name):
        return self.client().delete(self.base + f'/{name}',
                                    headers=self.headers)

    def test_new_algorithm(self):
        res = self.new_algorithm_missing_name()
        self.assertEqual(400, res.status_code)
        res = self.new_algorithm_missing_file('sometitle')
        self.assertEqual(400, res.status_code)
        res = self.new_algorithm('sometitle')
        self.assertEqual(201, res.status_code)
        res = self.new_algorithm('sometitle')
        self.assertEqual(409, res.status_code)

    def test_get_all_algorithms(self):
        res = self.get_all_algorithms(1, 4)
        self.assertEqual(400, res.status_code)
        res = self.get_all_algorithms(0, 10)
        self.assertEqual(400, res.status_code)
        res = self.get_all_algorithms(-4, 10)
        self.assertEqual(404, res.status_code)
        res = self.get_all_algorithms(1, 10)
        self.assertEqual(200, res.status_code)
        self.assertEqual(len(json_resp(res).get('datas')), 0)
        res = self.get_all_algorithms(134141, 11414)
        self.assertEqual(500, res.status_code)
        res = self.new_algorithm('sometitle')
        self.assertEqual(201, res.status_code)
        res = self.get_all_algorithms(1, 10)
        self.assertEqual(200, res.status_code)
        self.assertEqual(len(json_resp(res).get('datas')), 1)

    def test_get_algorithm(self):
        res = self.new_algorithm('sometitle')
        self.assertEqual(201, res.status_code)
        res = self.get_algorithm('sometitle')
        self.assertEqual(200, res.status_code)
        res = self.get_algorithm('hhh')
        self.assertEqual(404, res.status_code)
        res = self.get_algorithm(1231241341)
        self.assertEqual(404, res.status_code)
        res = self.get_algorithm_empty()
        self.assertEqual(405, res.status_code)

    def test_update_algorithm(self):
        res = self.new_algorithm('sometitle')
        self.assertEqual(201, res.status_code)
        uw = str(datetime.now())
        res = self.update_algorithm('bla', uw)
        self.assertEqual(404, res.status_code)
        res = self.update_algorithm('sometitle', uw)
        self.assertEqual(204, res.status_code)

    def test_delete_algorithm(self):
        res = self.new_algorithm('sometitle')
        self.assertEqual(201, res.status_code)
        res = self.delete_algorithm('bla')
        self.assertEqual(404, res.status_code)
        res = self.delete_algorithm('sometitle')
        self.assertEqual(204, res.status_code)

    # self.assertIn('Go to Borabora', str(res.data))
    # result_in_json = json.loads(rv.data.decode('utf-8').replace("'", "\""))
    #


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
