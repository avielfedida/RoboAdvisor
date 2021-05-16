import time
from urllib.parse import unquote

import pytest
from selenium.common.exceptions import TimeoutException

from selenium_tests.Config.config import TestData
from selenium_tests.Data.Paths import Paths
from selenium_tests.Pages.HomePage import HomePage
from selenium_tests.Pages.PortfolioPage import PortfolioPage
from selenium_tests.Pages.QuestionnairePage import QuestionnairePage
from selenium_tests.Pages.UserLatestResultsPage import UserLatestResultsPage
from selenium_tests.utils import get_portfolio_link_len


@pytest.mark.usefixtures("tear_up_down")
class Test_ModelCases:

    def model_execution(self):
        page = HomePage(self.driver)
        page.start_questionnaire()
        current_url = unquote(self.driver.current_url)
        page = QuestionnairePage(self.driver)
        assert current_url == unquote(self.driver.current_url)
        page.click_start_btn()

        for i in range(8):
            page.select_random_answer()
            page.select_random_model()
            page.next_question_click()

        try:
            page.is_low_risk_questionnaire()
        except TimeoutException as _:
            page.wait_until_url_contains(TestData.BASE_URL+Paths.PORTFOLIO)
            # [1] to take /link and [1:] to remove the /
            link = unquote(self.driver.current_url).split(TestData.BASE_URL+Paths.PORTFOLIO)[1][1:]
            assert len(link) == get_portfolio_link_len()
            return link
        return None

    # Repeat the test X times.
    # @pytest.mark.parametrize('execution_number', range(5))
    # def test_guest_model_execution(self):
    #     self.model_execution()

    # @pytest.mark.usefixtures("login_home_logout")
    # def test_logged_in_model_execution(self):
    #     link = self.model_execution()
    #     if link is not None:
    #         page = HomePage(self.driver)
    #         page.click_latest_results()
    #         assert page.is_first_table_link_is(link)
    #

    @pytest.mark.usefixtures("login_home_logout")
    def test_logged_in_model_execution_and_rebalance(self):
        link = self.model_execution()
        if link is not None:
            page = PortfolioPage(self.driver, link)
            page.do_rebalance()
            # Should redirect me to the latest results.
            page = UserLatestResultsPage(self.driver)
            assert page.is_first_table_link_is(link)
            for _ in range(TestData.TIMEOUT*5):
                page.click_refresh_btn()
                try:
                    assert page.is_second_table_link_is(link)
                    time.sleep(300000)
                    break
                except TimeoutException as _:
                    pass
            # page = HomePage(self.driver)
            # page.click_latest_results()
            # assert page.is_first_table_link_is(link)



