from selenium.webdriver.common.by import By

from selenium_tests.Config.config import TestData
from selenium_tests.Pages.BasePage import BasePage
from selenium_tests.utils import get_portfolio_url


class PortfolioPage(BasePage):
    REBALANCE_BTN = (By.ID, "rebalance_btn")
    PORTFOLIO_LINK = (By.ID, "portfolio_link")

    def __init__(self, driver, link):
        super().__init__(driver)
        self.PAGE_PATH = get_portfolio_url(link)
        self.driver.get(TestData.BASE_URL + self.PAGE_PATH)

    def do_rebalance(self):
        self.do_click(self.REBALANCE_BTN)
        self.ok_on_alert()

    def is_rebalance_btn_exists(self):
        return self.is_visible(self.REBALANCE_BTN)

    def is_portfolio_link_exists(self):
        return self.is_visible(self.PORTFOLIO_LINK)
