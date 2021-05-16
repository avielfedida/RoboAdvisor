from selenium.webdriver.common.by import By

from selenium_tests.Config.config import TestData
from selenium_tests.Data.Paths import Paths
from selenium_tests.Pages.BasePage import BasePage
from selenium_tests.utils import get_cluster_title_url, get_random_str


class NewPostPage(BasePage):
    NEW_POST_TITLE_FIELD = (By.ID, "new_post_title")
    NEW_POST_SUBMIT_BTN = (By.ID, "new_post_submit_btn")
    NEW_POST_CONTENT_FIELD_CONTAINER = (By.XPATH, "//div[@class='DraftEditor-editorContainer']")

    def __init__(self, driver, path):
        super().__init__(driver)
        self.PAGE_PATH = path
        self.driver.get(TestData.BASE_URL+self.PAGE_PATH)


    def is_new_post_title_field_exists(self):
        return self.is_visible(self.NEW_POST_TITLE_FIELD)

    def is_new_post_content_field_container_exists(self):
        return self.is_visible(self.NEW_POST_CONTENT_FIELD_CONTAINER)

    def is_new_post_submit_btn_exists(self):
        return self.is_visible(self.NEW_POST_SUBMIT_BTN)

    def click_new_post_submit_btn(self):
        self.do_click(self.NEW_POST_SUBMIT_BTN)

    def fill_random(self):
        title = get_random_str()
        content = get_random_str()
        self.do_send_keys(self.NEW_POST_TITLE_FIELD, title)
        self.do_tabs()
        self.do_text_chain(content)
        return title, content
