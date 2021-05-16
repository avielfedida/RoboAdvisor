from selenium_tests.Config.config import TestData
from selenium_tests.Data.Paths import Paths
from selenium_tests.Pages.BasePage import BasePage
from selenium.webdriver.common.by import By

from selenium_tests.Pages.PageWithLatestResults import PageWithLatestResults


class HomePage(PageWithLatestResults):
    USERNAME_TEXT = (By.ID, "username")
    START_QUESTIONNAIRE_BTN = (By.ID, "start_questionnaire")
    LATEST_RESULTS = (By.ID, "latest_results_table")
    FORUM_LINK = (By.ID, "nav_link_forum")
    INFO_CENTER_LINK = (By.ID, "nav_link_info_center")

    USER_PROFILE_NAV = (By.ID, "user_profile_nav")
    USER_LATEST_RESULTS_NAV = (By.ID, "user_latest_results_nav")
    USER_LOGOUT = (By.ID, "user_logout")

    PAGE_PATH = "/"


    def __init__(self, driver, wait_for_logged_in_user=False):
        super().__init__(driver)
        if wait_for_logged_in_user:
            self.is_visible(self.USERNAME_TEXT)
        self.driver.get(TestData.BASE_URL+self.PAGE_PATH)

    def logout(self):
        self.do_click(self.USERNAME_TEXT)
        self.is_visible(self.USER_LOGOUT) # Wait for it to load
        self.do_click(self.USER_LOGOUT)
        self.is_invisible(self.USERNAME_TEXT)
        self.refresh_page()


    def get_username_text(self):
        return self.get_element_text(self.USERNAME_TEXT)

    def click_edit_profile(self):
        self.do_click(self.USERNAME_TEXT)
        self.do_click(self.USER_PROFILE_NAV)

    def click_latest_results(self):
        self.do_click(self.USERNAME_TEXT)
        self.do_click(self.USER_LATEST_RESULTS_NAV)

    def navigate_to_forum(self):
        self.do_click(self.FORUM_LINK)

    def is_nav_forum_link_exists(self):
        return self.is_visible(self.FORUM_LINK)

    def is_nav_info_center_link_exists(self):
        return self.is_visible(self.INFO_CENTER_LINK)

    def is_username_text_exists(self):
        return self.is_visible(self.USERNAME_TEXT)

    def start_questionnaire(self):
        self.do_click(self.START_QUESTIONNAIRE_BTN)

    def is_start_questionnaire_btn_exists(self):
        return self.is_visible(self.START_QUESTIONNAIRE_BTN)

