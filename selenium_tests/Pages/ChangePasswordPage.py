from selenium.webdriver.common.by import By

from selenium_tests.Config.config import TestData
from selenium_tests.Data.Paths import Paths
from selenium_tests.Pages.BasePage import BasePage


class ChangePasswordPage(BasePage):
    CHANGE_PASSWORD_SUBMIT_BTN = (By.ID, "change_password_submit_btn")
    OLD_PASSWORD_FIELD = (By.ID, "old_password_field")
    NEW_PASSWORD_FIELD = (By.ID, "new_password_field")
    NEW_PASSWORD_REPEAT_FIELD = (By.ID, "new_password_repeat_field")
    SUCCESS_MESSAGE = (By.XPATH, "//span[@data-variant='success']")
    ERROR_MESSAGE = (By.XPATH, "//span[@data-variant='danger']")

    PAGE_PATH = Paths.CHANGE_PASSWORD

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
        return self.is_visible(self.CHANGE_PASSWORD_SUBMIT_BTN) and self.is_visible(self.OLD_PASSWORD_FIELD) and self.is_visible(self.NEW_PASSWORD_FIELD) and self.is_visible(self.NEW_PASSWORD_REPEAT_FIELD)

    def set_old_password(self, old_password):
        self.do_clear(self.OLD_PASSWORD_FIELD)
        self.do_send_keys(self.OLD_PASSWORD_FIELD, old_password)

    def set_new_password(self, new_password):
        self.do_clear(self.NEW_PASSWORD_FIELD)
        self.do_send_keys(self.NEW_PASSWORD_FIELD, new_password)

    def set_new_password_repeat(self, new_password_repeat):
        self.do_clear(self.NEW_PASSWORD_REPEAT_FIELD)
        self.do_send_keys(self.NEW_PASSWORD_REPEAT_FIELD, new_password_repeat)

    def submit_change_password(self):
        self.do_click(self.CHANGE_PASSWORD_SUBMIT_BTN)
