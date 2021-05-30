import unittest

from tests.test_base import TestBase


class MembersTest(TestBase):
    def setUp(self):
        super(MembersTest, self).setUp()
        self.base += '/members'
        # self.username1 = 'aviel@gmail.com'
        # self.password1 = 'pass'

        self.username1 = 'moran1@gmail.com'
        self.password1 = 'moran1'


    def tearDown(self):
        super(MembersTest, self).tearDown()

    def test_login_all_valid(self):
        # self.register()
        res = self.client().post(f'{self.base}/login',
                                 json=dict(email=self.username1, password=self.password1), headers=self.headers)
        self.assertEqual(200, res.status_code)

    # def test_login_wrong_mail(self):
    #     res = self.client().post(f'{self.base}/login',
    #                              json=dict(email='wrong@gmail.com', password=self.password1), headers=self.headers)
    #     self.assertEqual(401, res.status_code)
    #
    # def test_login_wrong_password(self):
    #     res = self.client().post(f'{self.base}/login',
    #                              json=dict(email=self.username1, password='wrongPass'), headers=self.headers)
    #     self.assertEqual(401, res.status_code)
    #
    # def test_update_names_all_valid(self):
    #     self.login(self.username1, self.password1)
    #     json = {
    #         "email": "noa@gmail.com",
    #         "password": "newPass",
    #         "first_name": "newFirst",
    #         "last_name": "newLast"}
    #     res = self.client().put(self.base + '/update_name', headers=self.headers, json=json)
    #     self.assertEqual(200, res.status_code)
    #
    # def test_update_first_name_all_valid(self):
    #     self.login(self.username1, self.password1)
    #     json = {
    #         "email": "noa@gmail.com",
    #         "password": "newPass",
    #         "first_name": "newFirst1",
    #         "last_name": "newLast"}
    #     res = self.client().put(self.base + '/update_name', headers=self.headers, json=json)
    #     self.assertEqual(200, res.status_code)
    #
    # def test_update_last_name_all_valid(self):
    #     self.login(self.username1, self.password1)
    #     json = {
    #         "email": "noa@gmail.com",
    #         "password": "newPass",
    #         "first_name": "newFirst1",
    #         "last_name": "newLast1"}
    #     res = self.client().put(self.base + '/update_name', headers=self.headers, json=json)
    #     self.assertEqual(200, res.status_code)
    #
    # def test_update_names_no_login(self):
    #     json = {
    #         "email": "aviel@gmail.com",
    #         "password": "newPass",
    #         "first_name": "newFirst1",
    #         "last_name": "newLast1"}
    #     res = self.client().put(self.base + '/update_name', headers=self.headers, json=json)
    #     self.assertEqual(401, res.status_code)
    #
    # def test_update_password_all_valid(self):
    #     self.login(self.username1, self.password1)
    #     json = {
    #         "password": "nao",
    #         "new_password": "newPass"}
    #     res = self.client().put(self.base + '/update_password', headers=self.headers, json=json)
    #     self.assertEqual(200, res.status_code)
    #
    # def test_update_password_no_login(self):
    #     json = {
    #         "password": "pass",
    #         "new_password": "newPass"}
    #     res = self.client().put(self.base + '/update_password', headers=self.headers, json=json)
    #     self.assertEqual(401, res.status_code)
    #
    # def test_update_password_same_password(self):
    #     self.login(self.username1, self.password1)
    #     json = {
    #         "password": "newPass",
    #         "new_password": "newPass"}
    #     res = self.client().put(self.base + '/update_password', headers=self.headers, json=json)
    #     self.assertEqual(409, res.status_code)
    #
    # def test_update_password_not_same_password_in_system(self):
    #     self.login(self.username1, self.password1)
    #     json = {
    #         "password": "noa",
    #         "new_password": "newPass"}
    #     res = self.client().put(self.base + '/update_password', headers=self.headers, json=json)
    #     self.assertEqual(401, res.status_code)


if __name__ == "__main__":
    unittest.main()
