from urllib.parse import unquote

from selenium.webdriver.common.by import By

from selenium_tests.Config.config import TestData
from selenium_tests.Data.Paths import Paths
from selenium_tests.Pages.BasePage import BasePage


class PageWithLatestResults(BasePage):

    def __init__(self, driver):
        super().__init__(driver)


    def get_k_table_link(self, k):
        locator = (By.XPATH, f"//table[@id='latest_results_table']//tbody/tr[{k}]/td[3]/a")
        elements = self.get_elements(locator)
        assert len(elements) > 0
        href_link = unquote(elements[0].get_attribute("href")).split(TestData.BASE_URL + Paths.PORTFOLIO)[1][1:]
        return href_link

    def is_first_table_link_is(self, link):
        return link == self.get_k_table_link(1)

    def is_second_table_link_is(self, link):
        return link == self.get_k_table_link(2)

