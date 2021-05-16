import pytest

from selenium_tests.Data.SiteMessages import SiteMessages
from selenium_tests.Pages.HomePage import HomePage
from selenium_tests.Pages.LoginPage import LoginPage
from selenium_tests.utils import get_random_username_password


@pytest.mark.usefixtures("tear_up_down")
class Test_HomePage:

    def test_crucial_elements_visibility(self):
        page = HomePage(self.driver)
        assert page.is_start_questionnaire_btn_exists()
        assert page.is_nav_forum_link_exists()
        assert page.is_nav_info_center_link_exists()

