import unittest

from tests.test_base import TestBase


class ClustersTest(TestBase):
    def setUp(self):
        super(ClustersTest, self).setUp()
        self.base += '/cluster'
        # self.add_clusters()

    def tearDown(self):
        super(ClustersTest, self).tearDown()

    def test_get_all_clusters_valid(self):
        return self.client().get(f'{self.base}/get_clusters',
                                 headers=self.headers)


if __name__ == "__main__":
    unittest.main()
