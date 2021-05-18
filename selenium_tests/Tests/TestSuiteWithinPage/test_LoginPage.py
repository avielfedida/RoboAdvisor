import pytest

from selenium_tests.Data.SiteMessages import SiteMessages
from selenium_tests.Pages.LoginPage import LoginPage
from selenium_tests.utils import get_random_username_password


@pytest.mark.usefixtures("tear_up_down")
class Test_LoginPage:

    def test_crucial_elements_visibility(self):
        page = LoginPage(self.driver)
        assert page.is_login_btn_exists()
        assert page.is_email_field_exists()
        assert page.is_password_field_exists()

    def test_not_logged_in(self):
        page = LoginPage(self.driver)
        page.do_login(*get_random_username_password())
        assert page.is_danger_presented()
        assert page.is_danger_message_equal(SiteMessages.INVALID_LOGIN_CREDENTIALS)
