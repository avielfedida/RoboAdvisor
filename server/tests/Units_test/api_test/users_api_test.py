import unittest

from tests.test_base import TestBase


class UsersTest(TestBase):
    def setUp(self):
        super(UsersTest, self).setUp()
        self.base += '/users'
        self.username1 = 'aviel@gmail.com'
        self.password1 = 'pass'

    def tearDown(self):
        super(UsersTest, self).tearDown()

    def test_register_all_valid(self):
        res = self.client().post(f'{self.base}/register',
                                 json=dict(email=self.username1, password=self.password1, first_name="avi",
                                           last_name="yoni"), headers=self.headers)
        self.assertEqual(200, res.status_code)

    def test_register_all_twice_same_username(self):
        res = self.client().post(f'{self.base}/register',
                                 json=dict(email=self.username1, password=self.password1, first_name="avi",
                                           last_name="yoni"), headers=self.headers)
        self.assertEqual(200, res.status_code)
        res = self.client().post(f'{self.base}/register',
                                 json=dict(email=self.username1, password=self.password1, first_name="avi",
                                           last_name="yoni"), headers=self.headers)
        self.assertEqual(409, res.status_code)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
