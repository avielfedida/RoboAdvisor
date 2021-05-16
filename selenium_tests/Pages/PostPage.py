from selenium.webdriver.common.by import By

from selenium_tests.Config.config import TestData
from selenium_tests.Pages.BasePage import BasePage


class PostPage(BasePage):
    NEW_MESSAGE_BTN = (By.ID, "new_message_btn")
    MESSAGE_LOCATOR = (By.XPATH, "//div[contains(@class, 'card-body')]")

    def __init__(self, driver, path):
        super().__init__(driver)
        self.PAGE_PATH = path
        self.driver.get(TestData.BASE_URL + self.PAGE_PATH)

    def is_new_message_btn(self):
        return self.is_visible(self.NEW_MESSAGE_BTN)

    def submit_new_message(self, content):
        self.send_text_to_draftjs(content)
        self.do_click(self.NEW_MESSAGE_BTN)

    def is_message_with_content_exists(self, content):
        locator = (By.XPATH, f"//span[@data-text='true'][contains(text(), '{content}')]")
        return self.is_visible(locator)
