import unittest

from tests.old_for_ref.test_base import TestBase
from tests.old_for_ref.utils import json_resp


class StudiesTestCase(TestBase):

    def setUp(self):
        super(StudiesTestCase, self).setUp()
        self.register_and_login()
        self.base += '/studies'
        self.in_sample = None
        self.oos = None

    def tearDown(self):
        if self.in_sample:
            self.in_sample.close()
        if self.oos:
            self.oos.close()
        super(StudiesTestCase, self).tearDown()


    def get_all_studies(self, page, perPage):
        return self.client().get(self.base + f'/{page}/{perPage}/',
                                 headers=self.headers)

    def get_study(self, study_id):
        return self.client().get(self.base + f'/{study_id}',
                                 headers=self.headers)

    def get_study_empty(self):
        return self.client().get(self.base + f'/',
                                 headers=self.headers)

    def delete_study(self, study_id):
        return self.client().delete(self.base + f'/{study_id}',
                                    headers=self.headers)

    def test_study_first_step(self):
        res = self.study_first_step("XAR", "15min time frame")
        self.assertEqual(200, res.status_code)
        # Should work again.
        res = self.study_first_step("XAR", "15min time frame")
        self.assertEqual(200, res.status_code)

    def test_study_submit(self):
        res = self.study_first_step("XAR", "15min time frame")
        self.assertEqual(200, res.status_code)
        token = json_resp(res).get('token')
        res = self.study_submit([], 'somescriptname', token)
        self.assertEqual(201, res.status_code)

    def test_get_all_studies(self):
        res = self.get_all_studies(1, 4)
        self.assertEqual(400, res.status_code)
        res = self.get_all_studies(0, 10)
        self.assertEqual(400, res.status_code)
        res = self.get_all_studies(-4, 10)
        self.assertEqual(404, res.status_code)
        res = self.get_all_studies(1, 10)
        self.assertEqual(200, res.status_code)
        self.assertEqual(len(json_resp(res).get('datas')), 0)
        res = self.get_all_studies(1341410, 110044)
        self.assertEqual(500, res.status_code)
        res = self.study_first_step("XAR", "15min time frame")
        self.assertEqual(200, res.status_code)
        token = json_resp(res).get('token')
        res = self.study_submit([], 'somescriptname', token)
        self.assertEqual(201, res.status_code)
        res = self.get_all_studies(1, 10)
        self.assertEqual(200, res.status_code)
        self.assertEqual(len(json_resp(res).get('datas')), 1)

    def test_get_study(self):
        res = self.study_first_step("XAR", "15min time frame")
        self.assertEqual(200, res.status_code)
        token = json_resp(res).get('token')
        res = self.study_submit([], 'somescriptname', token)
        self.assertEqual(201, res.status_code)
        study_id = json_resp(res).get('id')
        res = self.get_study(study_id)
        self.assertEqual(200, res.status_code)
        res = self.get_study(1231241341)
        self.assertEqual(404, res.status_code)
        res = self.get_study_empty()
        self.assertEqual(405, res.status_code)

    def test_delete_algorithm(self):
        res = self.study_first_step("XAR", "15min time frame")
        self.assertEqual(200, res.status_code)
        token = json_resp(res).get('token')
        res = self.study_submit([], 'somescriptname', token)
        self.assertEqual(201, res.status_code)
        study_id = json_resp(res).get('id')
        res = self.delete_study(1231241241)
        self.assertEqual(404, res.status_code)
        res = self.delete_study(study_id)
        self.assertEqual(204, res.status_code)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
