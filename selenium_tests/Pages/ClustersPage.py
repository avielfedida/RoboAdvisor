import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from selenium_tests.Config.config import TestData
from selenium_tests.Data.Paths import Paths
from selenium_tests.Pages.BasePage import BasePage


class ClustersPage(BasePage):
    CLUSTER_BANNER_IMAGES = (By.CLASS_NAME, "forum_cluster")
    CLUSTERS_BTNS = (By.XPATH, "//div[contains(@class, 'card-body')]/button")
    CLUSTERS_TITLES = (By.XPATH, "//div[contains(@class, 'card-title')]")
    PAGE_PATH = Paths.FORUM


    def __init__(self, driver):
        super().__init__(driver)
        self.driver.get(TestData.BASE_URL+self.PAGE_PATH)

    def get_first_cluster_title(self):
        elements = self.get_elements(self.CLUSTERS_TITLES)
        assert len(elements) > 0
        return elements[0].text

    def get_number_of_clusters(self):
        return self.get_number_of_elements(self.CLUSTER_BANNER_IMAGES)

    def click_first_cluster(self):
        elements = self.get_elements(self.CLUSTERS_BTNS)
        assert len(elements) > 0
        elements[0].click()

    def start_questionnaire(self):
        self.do_click(self.START_QUESTIONNAIRE_BTN)

    def is_start_questionnaire_btn_exists(self):
        return self.is_visible(self.START_QUESTIONNAIRE_BTN)

