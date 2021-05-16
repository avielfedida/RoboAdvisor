from selenium.webdriver.common.by import By
import random
from selenium_tests.Config.config import TestData
from selenium_tests.Data.Paths import Paths
from selenium_tests.Pages.BasePage import BasePage


class QuestionnairePage(BasePage):
    QT_EXPLANATION_START_BTN = (By.ID, "qt_explanation_start_btn")
    MODELS_RADIO_OPTIONS = (By.ID, "models_radio_options")
    ANSWERS_RADIO_OPTIONS = (By.ID, "answers_radio_options")
    NEXT_QUESTION_BTN = (By.ID, "next_question_btn")
    PREVIOUS_QUESTION_BTN = (By.ID, "previous_question_btn")

    LOW_RISK_QUESTIONNAIRE = (By.ID, "low_risk_explanation_screen")

    PAGE_PATH = Paths.QUESTIONNAIRE_EXPLANATION

    def __init__(self, driver):
        super().__init__(driver)
        self.driver.get(TestData.BASE_URL + self.PAGE_PATH)

    def is_low_risk_questionnaire(self):
        return self.is_visible(self.LOW_RISK_QUESTIONNAIRE, TestData.REDUCED_TIMEOUT)

    def get_radio_elements_in_container_by_id(self, container_id):
        return self.get_elements((By.XPATH, f"//div[@id='{container_id}']//input[@type='radio']"))

    def select_random_model(self):
        m_elements = self.get_radio_elements_in_container_by_id("models_radio_options")
        assert len(m_elements) > 0
        random.choice(m_elements).click()

    def select_random_answer(self):
        q_elements = self.get_radio_elements_in_container_by_id("answers_radio_options")
        assert len(q_elements) > 0
        random.choice(q_elements).click()

    def next_question_click(self):
        self.do_click(self.NEXT_QUESTION_BTN)

    def previous_question_click(self):
        self.do_click(self.PREVIOUS_QUESTION_BTN)

    def is_qt_explanation_start_btn(self):
        return self.is_visible(self.QT_EXPLANATION_START_BTN)

    def is_questionnaire_shown(self):
        return self.is_visible(self.MODELS_RADIO_OPTIONS) and self.is_visible(self.ANSWERS_RADIO_OPTIONS) and self.is_visible(self.NEXT_QUESTION_BTN) and self.is_visible(self.PREVIOUS_QUESTION_BTN)

    def click_start_btn(self):
        self.do_click(self.QT_EXPLANATION_START_BTN)