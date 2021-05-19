from tests.test_base import TestBase
import unittest
import uuid


class TopicsTest(TestBase):
    def setUp(self):
        super(TopicsTest, self).setUp()
        self.base += '/topics'
        self.username1 = 'loa8@gmail.com'
        self.password1 = 'pass8'

    def tearDown(self):
        super(TopicsTest, self).tearDown()

    def test_post_single_topic_all_valid(self):
        # self.register(self.username1, self.password1)
        self.login(self.username1, self.password1)
        json = {
            "title": str(uuid.uuid4()),
            "cluster_title": "title1",
            "message": "bla"
        }
        res = self.client().post(self.base + '/single_topic', headers=self.headers, json=json)
        self.assertEqual(200, res.status_code)

    def test_post_single_topic_no_title(self):
        # self.register()
        self.login(self.username1, self.password1)
        json = {
            "title": "",
            "cluster_title": "title1",
            "message": "bla"
        }
        res = self.client().post(self.base + '/single_topic', headers=self.headers, json=json)
        self.assertEqual(400, res.status_code)

    def test_post_single_topic_no_cluster_title(self):
        # self.register()
        self.login(self.username1, self.password1)
        json = {
            "title": "title",
            "cluster_title": "",
            "message": "bla"
        }
        res = self.client().post(self.base + '/single_topic', headers=self.headers, json=json)
        self.assertEqual(400, res.status_code)

    def test_post_single_topic_wrong_cluster_title(self):
        # self.register()
        self.login(self.username1, self.password1)
        json = {
            "title": "title",
            "cluster_title": "title3",
            "message": "bla"
        }
        res = self.client().post(self.base + '/single_topic', headers=self.headers, json=json)
        self.assertEqual(500, res.status_code)

    def test_get_all_topics_all_valid(self):
        res = self.client().get(self.base + f'/all/1/title1', headers=self.headers)
        self.assertEqual(200, res.status_code)

    def test_get_all_topics_zero_pages(self):
        res = self.client().get(self.base + f'/all/0/title1', headers=self.headers)
        self.assertEqual(400, res.status_code)


if __name__ == "__main__":
    unittest.main()
