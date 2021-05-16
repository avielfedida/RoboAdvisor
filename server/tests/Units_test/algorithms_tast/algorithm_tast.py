import unittest
from tests.test_base import TestBase
import logging

from celery_tasks.worker_tasks import execute_models
from models.portfolio import Portfolio


class AlgorithmTestCase(TestBase):
    def setUp(self):
        super(AlgorithmTestCase, self).setUp()

    def test_execute_models(self):
        execute_models()
        models_names = ['markowitz', 'Kmeans', 'blackLitterman', 'mean_gini']
        risks = range(1, 6)
        for model in models_names:
            for risk in risks:
                portfolio = self.db.session.query(Portfolio).filter_by( algorithm=model, risk=risk).first()
                print(portfolio.as_dict())
                self.assertIsNotNone(portfolio)


if __name__ == "__main__":
    logging.disable(logging.CRITICAL)
    unittest.main()
