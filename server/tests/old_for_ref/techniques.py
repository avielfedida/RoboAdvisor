import unittest

from tests.old_for_ref.test_base import TestBase
from tests.old_for_ref.utils import json_resp


class TechniquesTestCase(TestBase):

    def setUp(self):
        super(TechniquesTestCase, self).setUp()
        self.register_and_login()
        self.base += '/techniques'


    # def tearDown(self):
    #     print('child tear down')
    #     super(TechniquesTestCase, self).tearDown()



    def new_tech_missing_title(self):
        return self.client().post(self.base + '/', headers=self.headers, json={
            'description': 'another title'
        })

    def new_tech_missing_description(self, title):
        return self.client().post(self.base + '/', headers=self.headers, json={
            'title': title,
        })

    def get_all_techs(self, page, perPage):
        return self.client().get(self.base + f'/{page}/{perPage}/',
                                 headers=self.headers)

    def get_tech(self, title):
        return self.client().get(self.base + f'/{title}',
                                 headers=self.headers)

    def get_tech_empty(self):
        return self.client().get(self.base + f'/',
                                 headers=self.headers)

    def update_technique(self, title, new_desc):
        return self.client().patch(self.base + f'/{title}',
                                   headers=self.headers, json={
                'description': new_desc
            })

    def delete_technique(self, title):
        return self.client().delete(self.base + f'/{title}',
                                    headers=self.headers)


    def test_new_tech(self):
        res = self.new_tech_missing_title()
        self.assertEqual(res.status_code, 400)
        res = self.new_tech_missing_description('some title')
        self.assertEqual(res.status_code, 400)
        res = self.new_tech('some title')
        self.assertEqual(res.status_code, 201)
        res = self.new_tech('some title')
        self.assertEqual(res.status_code, 409)

    def test_get_tech(self):
        res = self.new_tech('some title')
        self.assertEqual(res.status_code, 201)
        res = self.get_tech('some title')
        self.assertEqual(res.status_code, 200)
        res = self.get_tech('hhh')
        self.assertEqual(res.status_code, 404)
        res = self.get_tech_empty()
        self.assertEqual(res.status_code, 405)

    def test_get_all_techniques(self):
        res = self.get_all_techs(1, 4)
        self.assertEqual(res.status_code, 400)
        res = self.get_all_techs(0, 10)
        self.assertEqual(res.status_code, 400)
        res = self.get_all_techs(-4, 10)
        self.assertEqual(res.status_code, 404)
        res = self.get_all_techs(1, 10)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(json_resp(res).get('datas')), 0)
        res = self.get_all_techs(134141, 11414)
        self.assertEqual(res.status_code, 500)
        res = self.new_tech('some title')
        self.assertEqual(res.status_code, 201)
        res = self.get_all_techs(1, 10)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(json_resp(res).get('datas')), 1)

    def test_update_technique(self):
        res = self.new_tech('some title')
        self.assertEqual(res.status_code, 201)
        res = self.update_technique('bla', 'qweq')
        self.assertEqual(res.status_code, 404)
        res = self.update_technique('some title', 'qweq')
        self.assertEqual(res.status_code, 204)

    def test_delete_technique(self):
        res = self.new_tech('some title')
        self.assertEqual(res.status_code, 201)
        res = self.delete_technique('bla')
        self.assertEqual(res.status_code, 404)
        res = self.delete_technique('some title')
        self.assertEqual(res.status_code, 204)

        # self.assertIn('Go to Borabora', str(res.data))
        # result_in_json = json.loads(rv.data.decode('utf-8').replace("'", "\""))
        #

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
