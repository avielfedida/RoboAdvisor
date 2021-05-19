import unittest
from tests.test_base import TestBase


class MessagesTest(TestBase):
    def setUp(self):
        super(MessagesTest, self).setUp()
        self.base += '/topics'
        self.username1 = 'loa3@gmail.com'
        self.password1 = 'pass3'

    def tearDown(self):
        super(MessagesTest, self).tearDown()

    def test_register_all_valid(self):
        res = self.client().post(f'{self.base}/register',
                                 json=dict(email=self.username1, password=self.password1, first_name="avi",
                                           last_name="yoni"), headers=self.headers)
        self.assertEqual(200, res.status_code)


if __name__ == "__main__":
    unittest.main()
