from tests.test_base import TestBase
import unittest


class TopicsTest(TestBase):
    def setUp(self):
        super(TopicsTest, self).setUp()
        self.base += '/topics'
        self.username1 = 'loa3@gmail.com'
        self.password1 = 'pass3'

    def tearDown(self):
        super(TopicsTest, self).tearDown()

    def test_post_single_topic_all_valid(self):
        self.register()
        self.login(self.username1, self.password1)
        json = {
            "title": "test",
            "cluster_title": "title1",
            "message": "bla"
        }
        res = self.client().post(self.base + '/single_topic', headers=self.headers, json=json)
        self.assertEqual(200, res.status_code)

    def test_post_single_topic_no_title(self):
        self.register()
        self.login(self.username1, self.password1)
        json = {
            "title": "",
            "cluster_title": "title1",
            "message": "bla"
        }
        res = self.client().post(self.base + '/single_topic', headers=self.headers, json=json)
        self.assertEqual(400, res.status_code)

    def test_post_single_topic_no_cluster_title(self):
        self.register()
        self.login(self.username1, self.password1)
        json = {
            "title": "title",
            "cluster_title": "",
            "message": "bla"
        }
        res = self.client().post(self.base + '/single_topic', headers=self.headers, json=json)
        self.assertEqual(400, res.status_code)

    def test_post_single_topic_wrong_cluster_title(self):
        self.register()
        self.login(self.username1, self.password1)
        json = {
            "title": "title",
            "cluster_title": "title3",
            "message": "bla"
        }
        res = self.client().post(self.base + '/single_topic', headers=self.headers, json=json)
        self.assertEqual(500, res.status_code)

    def test_get_single_topic_all_valid(self):
        json = {
            "title": "test",
            "cluster_title": "title1",
        }
        res = self.client().get(self.base + '/get_single_topic', headers=self.headers, json=json)
        self.assertEqual(200, res.status_code)


if __name__ == "__main__":
    unittest.main()
