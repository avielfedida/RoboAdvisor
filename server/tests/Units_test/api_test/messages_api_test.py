import unittest
from tests.test_base import TestBase


class MessagesTest(TestBase):
    def setUp(self):
        super(MessagesTest, self).setUp()
        self.base += '/messages'
        self.username1 = 'loa3@gmail.com'
        self.password1 = 'pass3'

    def tearDown(self):
        super(MessagesTest, self).tearDown()

    def test_post_single_message_all_valid(self):
        self.login(self.username1, self.password1)
        json = {
            "content": "test",
            "topic_id": "2"}
        res = self.client().post(self.base + '/single_message', headers=self.headers, json=json)
        self.assertEqual(200, res.status_code)

    def test_post_single_message_empty_content(self):
        self.login(self.username1, self.password1)
        json = {
            "content": "",
            "topic_id": "2"}
        res = self.client().post(self.base + '/single_message', headers=self.headers, json=json)
        self.assertEqual(400, res.status_code)

    def test_post_single_message_empty_topic_id(self):
        self.login(self.username1, self.password1)
        json = {
            "content": "ok",
            "topic_id": ""}
        res = self.client().post(self.base + '/single_message', headers=self.headers, json=json)
        self.assertEqual(400, res.status_code)

    def test_post_single_message_empty_cant_message(self):
        self.login(self.username1, self.password1)
        json = {
            "content": "ok",
            "topic_id": "1"}
        res = self.client().post(self.base + '/single_message', headers=self.headers, json=json)
        self.assertEqual(500, res.status_code)

    def test_put_single_message_all_valid(self):
        self.login(self.username1, self.password1)
        json = {
            "id": "8",
            "content": "ok ok ok",
            "topic_id": "2"}
        res = self.client().put(self.base + '/single_message', headers=self.headers, json=json)
        self.assertEqual(200, res.status_code)

    def test_put_single_message_wrong_massageID(self):
        self.login(self.username1, self.password1)
        json = {
            "id": "1",
            "content": "ok ok ok",
            "topic_id": "2"}
        res = self.client().put(self.base + '/single_message', headers=self.headers, json=json)
        self.assertEqual(404, res.status_code)

    def test_put_single_message_wrong_topicID(self):
        self.login(self.username1, self.password1)
        json = {
            "id": "1",
            "content": "ok ok ok",
            "topic_id": "5"}
        res = self.client().put(self.base + '/single_message', headers=self.headers, json=json)
        self.assertEqual(404, res.status_code)

    def test_put_single_message_empty_content(self):
        self.login(self.username1, self.password1)
        json = {
            "id": "8",
            "content": "",
            "topic_id": "2"}
        res = self.client().put(self.base + '/single_message', headers=self.headers, json=json)
        self.assertEqual(400, res.status_code)

    def test_get_single_message_all_valid(self):
        res = self.client().get(self.base + '/single/2/8', headers=self.headers)
        self.assertEqual(200, res.status_code)

    def test_get_single_message_wrong_topicID(self):
        res = self.client().get(self.base + '/single/3/8', headers=self.headers)
        self.assertEqual(404, res.status_code)

    def test_get_single_message_wrong_messageID(self):
        res = self.client().get(self.base + '/single/2/2', headers=self.headers)
        self.assertEqual(404, res.status_code)

    def test_get_all_message_all_valid(self):
        res = self.client().get(self.base + '/all/2/1', headers=self.headers)
        self.assertEqual(200, res.status_code)

    def test_get_all_message_(self):
        res = self.client().get(self.base + '/all/2/0', headers=self.headers)
        self.assertEqual(400, res.status_code)


if __name__ == "__main__":
    unittest.main()
