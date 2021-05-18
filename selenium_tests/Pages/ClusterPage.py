from selenium.webdriver.common.by import By

from selenium_tests.Config.config import TestData
from selenium_tests.Data.Paths import Paths
from selenium_tests.Pages.BasePage import BasePage
from selenium_tests.utils import get_cluster_title_url


class ClusterPage(BasePage):
    NEW_POST_BTN = (By.ID, "new_post_btn")
    FORUM_SUBJECT = (By.XPATH, "//div[contains(@class, 'forum_subject_container')]")
    SUBJECT_TITLES = (By.XPATH, "//div[contains(@class, 'card-title')]")
    PAGE_PATH = Paths.FORUM


    def __init__(self, driver, title):
        super().__init__(driver)
        self.PAGE_PATH = get_cluster_title_url(title)
        self.driver.get(TestData.BASE_URL+self.PAGE_PATH)

    def click_post_title_link_return_href(self, title):
        locator = (By.XPATH, f"//div[contains(@class, 'card-title')][contains(text(), '{title}')]/../a")
        elements = self.get_elements(locator)
        assert len(elements) > 0
        href = elements[0].get_attribute("href")
        elements[0].click()
        return href


    def get_first_title(self):
        elements = self.get_elements(self.SUBJECT_TITLES)
        assert len(elements) > 0
        return elements[0].text

    def get_number_of_posts(self):
        return self.get_number_of_elements(self.FORUM_SUBJECT)

    def is_new_post_btn_exists(self):
        return self.is_visible(self.NEW_POST_BTN)

    def click_new_post_btn(self):
        self.do_click(self.NEW_POST_BTN)