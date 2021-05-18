from selenium.webdriver.common.by import By

from selenium_tests.Config.config import TestData
from selenium_tests.Data.Paths import Paths
from selenium_tests.Pages.BasePage import BasePage


class EditProfilePage(BasePage):
    EDIT_PROFILE_SUBMIT_BTN = (By.ID, "edit_profile_submit_btn")
    CHANGE_PASSWORD_PAGE_NAV = (By.ID, "change_password_page_nav")
    FIRST_NAME_FIELD = (By.ID, "first_name_field")
    LAST_NAME_FIELD = (By.ID, "last_name_field")
    SUCCESS_MESSAGE = (By.XPATH, "//span[@data-variant='success']")
    ERROR_MESSAGE = (By.XPATH, "//span[@data-variant='danger']")
    PAGE_PATH = Paths.PROFILE

    def __init__(self, driver):
        super().__init__(driver)
        self.driver.get(TestData.BASE_URL + self.PAGE_PATH)

    def is_success_presented(self):
        return self.is_visible(self.SUCCESS_MESSAGE)

    def is_success_message_equal(self, text):
        return self.get_element_text(self.SUCCESS_MESSAGE) == text

    def is_danger_presented(self):
        return self.is_visible(self.ERROR_MESSAGE)

    def is_danger_message_equal(self, text):
        return self.get_element_text(self.ERROR_MESSAGE) == text

    def all_elements_exists(self):
        return self.is_visible(self.EDIT_PROFILE_SUBMIT_BTN) and self.is_visible(
            self.FIRST_NAME_FIELD) and self.is_visible(self.LAST_NAME_FIELD) and self.is_visible(
            self.CHANGE_PASSWORD_PAGE_NAV)

    def nav_change_password_page(self):
        self.do_click(self.CHANGE_PASSWORD_PAGE_NAV)

    def set_first_name(self, new_first_name):
        self.do_clear(self.FIRST_NAME_FIELD)
        self.do_send_keys(self.FIRST_NAME_FIELD, new_first_name)

    def set_last_name(self, new_last_name):
        self.do_clear(self.LAST_NAME_FIELD)
        self.do_send_keys(self.LAST_NAME_FIELD, new_last_name)

    def submit_changes(self):
        self.do_click(self.EDIT_PROFILE_SUBMIT_BTN)
