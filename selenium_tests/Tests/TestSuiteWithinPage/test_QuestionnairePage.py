import pytest

from selenium_tests.Data.SiteMessages import SiteMessages
from selenium_tests.Data.TemplateData import TemplateData
from selenium_tests.Pages.QuestionnairePage import QuestionnairePage
from selenium_tests.Pages.RegisterPage import RegisterPage
from selenium_tests.utils import get_random_username_password


@pytest.mark.usefixtures("tear_up_down")
class Test_QuestionnairePage:

    def test_crucial_elements_visibility(self):
        page = QuestionnairePage(self.driver)
        assert page.is_qt_explanation_start_btn()
        page.click_start_btn()
        assert page.is_questionnaire_shown()

