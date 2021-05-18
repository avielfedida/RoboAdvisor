import unittest
from tests.test_base import TestBase
import logging


class ArticlesTestCase(TestBase):
    def setUp(self):
        super(ArticlesTestCase, self).setUp()
        # self.add_articles()
        self.base += '/articles'

    def test_get_all_articles(self):
        res = self.client().get(self.base + '/get_articles', headers=self.headers)
        self.assertEqual(res.status_code, 200)

    def test_get_article_by_valide_article_id(self):
        article_id = 1
        res = self.client().get(self.base + '/get_article' + f'/{article_id}', headers=self.headers)
        self.assertEqual(res.status_code, 200)

    def test_get_article_by_not_valide_article_id(self):
        article_id = -1
        res = self.client().get(self.base + '/get_article' + f'/{article_id}', headers=self.headers)
        self.assertEqual(res.status_code, 404)
        article_id = 100
        res = self.client().get(self.base + '/get_article' + f'/{article_id}', headers=self.headers)
        self.assertEqual(res.status_code, 404)


if __name__ == "__main__":
    logging.disable(logging.CRITICAL)
    unittest.main()
