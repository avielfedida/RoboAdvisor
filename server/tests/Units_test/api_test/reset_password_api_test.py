import unittest
from tests.test_base import TestBase
import logging


class ResetPasswordTestCase(TestBase):
    def setUp(self):
        super(ResetPasswordTestCase, self).setUp()
        self.base += '/reset_password'
        # self.register()

    def test_reset_password_by_email(self):
        json = {'email': 'patkennedy79@gmail.com'}
        res = self.client().post(self.base + '/request', headers=self.headers, json=json)
        self.assertEqual(res.status_code, 200)

    def test_reset_password_by_email_not_valid(self):
        json = {'email': 'patkennedy@gmail.com'}
        res = self.client().post(self.base + '/request', headers=self.headers, json=json)
        self.assertEqual(res.status_code, 409)

    def test_reset_password_enter_new_password_valid_id(self):
        json = {
            'id': '99756181-a520-4567-a221-cf7fa62e97bc',
            'new_password': '1234'
        }
        res = self.client().put(self.base + '/set_new_password', headers=self.headers, json=json)
        self.assertEqual(res.status_code, 200)
        json = {
            'id': '99756181-a520-4567-a221-cf7fa62e97bc',
            'new_password': '1234'
        }
        res = self.client().put(self.base + '/set_new_password', headers=self.headers, json=json)
        self.assertEqual(res.status_code, 401)

    def test_reset_password_enter_new_password_not_valid_id(self):
        json = {
            'id': '38c64ffe-b65c-4c39-a7b',
            'new_password': '1234'
        }
        res = self.client().put(self.base + '/set_new_password', headers=self.headers, json=json)
        self.assertEqual(res.status_code, 404)


if __name__ == "__main__":
    logging.disable(logging.CRITICAL)
    unittest.main()