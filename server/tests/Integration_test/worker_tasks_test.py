import unittest
from tests.test_base import TestBase
import logging

from celery_tasks.worker_tasks import execute_models, insert_price_data
from models.portfolio import Portfolio
from models.stock_price import StockPrice


class WorkerTasksTestCase(TestBase):
    def setUp(self):
        super(WorkerTasksTestCase, self).setUp()

    def test_execute_models(self):
        count_portfolio_old = self.db.session.query(Portfolio).count()
        count_stock_price_old = self.db.session.query(StockPrice).count()

        insert_price_data()
        execute_models()

        count_portfolio_new = self.db.session.query(Portfolio).count()
        count_stock_price_new = self.db.session.query(StockPrice).count()

        self.assertGreater(count_portfolio_new, count_portfolio_old)
        self.assertGreater(count_stock_price_new, count_stock_price_old)


if __name__ == "__main__":
    logging.disable(logging.CRITICAL)
    unittest.main()