from selenium.webdriver.common.by import By

from selenium_tests.Config.config import TestData
from selenium_tests.Data.Paths import Paths
from selenium_tests.Pages.BasePage import BasePage


class RegisterPage(BasePage):
    EMAIL = (By.ID, "email_field")
    PASSWORD = (By.ID, "password_field")
    PASSWORD_REPEAT = (By.ID, "password_repeat_field")
    FIRST_NAME = (By.ID, "first_name_field")
    LAST_NAME = (By.ID, "last_name_field")
    BIRTH_DATE = (By.ID, "birth_date_field")
    SUBMIT_BTN = (By.ID, "submit_btn")
    ERROR_MESSAGE = (By.XPATH, "//span[@data-variant='danger']")
    SUCCESS_MESSAGE = (By.XPATH, "//span[@data-variant='success']")
    PAGE_PATH = Paths.REGISTER

    def __init__(self, driver):
        super().__init__(driver)
        self.driver.get(TestData.BASE_URL + self.PAGE_PATH)

    def do_register(self, username, password, first_name, last_name, birth_date):
        self.do_send_keys(self.EMAIL, username)
        self.do_send_keys(self.PASSWORD, password)
        self.do_send_keys(self.PASSWORD_REPEAT, password)
        self.do_send_keys(self.FIRST_NAME, first_name)
        self.do_send_keys(self.LAST_NAME, last_name)
        self.do_send_keys(self.BIRTH_DATE, birth_date)
        self.do_click(self.SUBMIT_BTN)

    def reset_fields(self):
        self.do_clear(self.EMAIL)
        self.do_clear(self.PASSWORD)
        self.do_clear(self.PASSWORD_REPEAT)
        self.do_clear(self.FIRST_NAME)
        self.do_clear(self.LAST_NAME)
        self.do_clear(self.BIRTH_DATE)


    def is_register_btn_exists(self):
        return self.is_visible(self.SUBMIT_BTN)

    def is_email_field_exists(self):
        return self.is_visible(self.EMAIL)

    def is_password_field_exists(self):
        return self.is_visible(self.PASSWORD)

    def is_password_repeat_field_exists(self):
        return self.is_visible(self.PASSWORD_REPEAT)

    def is_birth_date_field_exists(self):
        return self.is_visible(self.BIRTH_DATE)

    def is_first_name_field_exists(self):
        return self.is_visible(self.FIRST_NAME)

    def is_last_name_field_exists(self):
        return self.is_visible(self.LAST_NAME)

    def is_danger_presented(self):
        return self.is_visible(self.ERROR_MESSAGE)

    def is_danger_not_presented(self):
        return self.is_invisible(self.ERROR_MESSAGE)

    def is_success_presented(self):
        return self.is_visible(self.SUCCESS_MESSAGE)

    def is_danger_message_equal(self, text):
        return self.get_element_text(self.ERROR_MESSAGE) == text

    def is_success_message_equal(self, text):
        return self.get_element_text(self.SUCCESS_MESSAGE) == text
