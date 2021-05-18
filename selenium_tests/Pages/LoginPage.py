from selenium_tests.Config.config import TestData
from selenium_tests.Data.Paths import Paths
from selenium_tests.Pages.BasePage import BasePage
from selenium.webdriver.common.by import By

class LoginPage(BasePage):
    EMAIL = (By.ID, "email_field")
    PASSWORD = (By.ID, "password_field")
    SUBMIT_BTN = (By.ID, "submit_btn")
    ERROR_MESSAGE = (By.XPATH, "//span[@data-variant='danger']")
    PAGE_PATH = Paths.LOGIN


    def __init__(self, driver):
        super().__init__(driver)
        self.driver.get(TestData.BASE_URL+self.PAGE_PATH)

    def do_login(self, username, password):
        self.do_send_keys(self.EMAIL, username)
        self.do_send_keys(self.PASSWORD, password)
        self.do_click(self.SUBMIT_BTN)

    def is_login_btn_exists(self):
        return self.is_visible(self.SUBMIT_BTN)

    def is_email_field_exists(self):
        return self.is_visible(self.EMAIL)

    def is_password_field_exists(self):
        return self.is_visible(self.PASSWORD)

    def is_danger_presented(self):
        return self.is_visible(self.ERROR_MESSAGE)

    def is_danger_message_equal(self, text):
        return self.get_element_text(self.ERROR_MESSAGE) == text