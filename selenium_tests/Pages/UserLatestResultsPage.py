from selenium.webdriver.common.by import By

from selenium_tests.Config.config import TestData
from selenium_tests.Pages.PageWithLatestResults import PageWithLatestResults


class UserLatestResultsPage(PageWithLatestResults):
    REFRESH_BTN = (By.ID, "refresh_latest_results")
    USER_LATEST_RESULTS_NAV = (By.ID, "user_latest_results_nav")
    PAGE_PATH = "/user_latest_results"

    def __init__(self, driver):
        super().__init__(driver)
        self.driver.get(TestData.BASE_URL + self.PAGE_PATH)

    def click_refresh_btn(self):
        self.do_click(self.REFRESH_BTN)

    def is_refresh_btn_exists(self):
        return self.is_visible(self.REFRESH_BTN)

    # def is_message_with_content_exists(self, content):
    #     locator = (By.XPATH, f"//span[@data-text='true'][contains(text(), '{content}')]")
    #     return self.is_visible(locator)
