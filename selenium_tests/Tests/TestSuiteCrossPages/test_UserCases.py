import time
from urllib.parse import unquote

import pytest

from selenium_tests.Config.config import TestData
from selenium_tests.Data.Paths import Paths
from selenium_tests.Data.SiteMessages import SiteMessages
from selenium_tests.Data.TemplateData import TemplateData
from selenium_tests.Pages.ChangePasswordPage import ChangePasswordPage
from selenium_tests.Pages.EditProfilePage import EditProfilePage
from selenium_tests.Pages.LoginPage import LoginPage
from selenium_tests.Pages.HomePage import HomePage
from selenium_tests.Pages.RegisterPage import RegisterPage
from selenium_tests.utils import get_random_username_password, get_random_str


@pytest.mark.usefixtures("tear_up_down")
class Test_UserCases:

    def test_register_then_login(self):
        # Move to register page
        page = RegisterPage(self.driver)
        username, password = get_random_username_password()
        page.do_register(username=username, password=password, birth_date=TemplateData.BIRTH_DATE,
                         first_name=TemplateData.FIRST_NAME, last_name=TemplateData.LAST_NAME)
        assert page.is_success_presented()
        assert page.is_success_message_equal(SiteMessages.REGISTER_SUCCESSFULLY)

        # Move to login page
        page = LoginPage(self.driver)
        page.do_login(username, password)

        # Move to the main page (should be moved automatically but we don't want to count on that)
        page = HomePage(self.driver, wait_for_logged_in_user=True)
        assert page.is_username_text_exists()
        page.logout()


    @pytest.mark.usefixtures("login_home_logout")
    def test_register_login_and_update_first_last_name_fail(self, login_home_logout):
        username, password, page = login_home_logout
        page.click_edit_profile()
        page = EditProfilePage(self.driver)
        page.set_first_name("")
        page.set_last_name(TemplateData.UPDATE_LAST_NAME)
        page.submit_changes()
        assert page.is_danger_presented()
        assert page.is_danger_message_equal(SiteMessages.FIRST_NAME_CANT_BE_EMPTY)

        page.set_first_name(TemplateData.UPDATE_FIRST_NAME)
        page.set_last_name("")
        page.submit_changes()
        assert page.is_danger_presented()
        assert page.is_danger_message_equal(SiteMessages.LAST_NAME_CANT_BE_EMPTY)


    @pytest.mark.usefixtures("login_home_logout")
    def test_register_login_and_change_password_fail(self, login_home_logout):
        username, password, page = login_home_logout
        page = EditProfilePage(self.driver)
        page.nav_change_password_page()
        assert TestData.BASE_URL+Paths.CHANGE_PASSWORD == unquote(self.driver.current_url)
        page = ChangePasswordPage(self.driver)
        new_password = get_random_str()
        page.set_old_password("")
        page.set_new_password(new_password)
        page.set_new_password_repeat(new_password)
        page.submit_change_password()
        assert page.is_danger_presented()
        assert page.is_danger_message_equal(SiteMessages.ENTER_OLD_PASSWORD)
        page.set_old_password(password)
        page.set_new_password("")
        page.set_new_password_repeat(new_password)
        page.submit_change_password()
        assert page.is_danger_presented()
        assert page.is_danger_message_equal(SiteMessages.PASSWORD_CANNOT_BE_EMPTY)
        page.set_old_password(password)
        page.set_new_password(new_password)
        page.set_new_password_repeat("")
        page.submit_change_password()
        assert page.is_danger_presented()
        assert page.is_danger_message_equal(SiteMessages.PASSWORD_DO_NOT_MATCH)

    @pytest.mark.usefixtures("login_home_logout")
    def test_register_login_and_update_first_last_name(self, login_home_logout):
        username, password, page = login_home_logout
        page.click_edit_profile()
        page = EditProfilePage(self.driver)
        page.set_first_name(TemplateData.UPDATE_FIRST_NAME)
        page.set_last_name(TemplateData.UPDATE_LAST_NAME)
        page.submit_changes()
        assert page.is_success_presented()
        assert page.is_success_message_equal(SiteMessages.PROFILE_UPDATED_SUCCESSFULLY)
        page = HomePage(self.driver, wait_for_logged_in_user=True)
        assert page.get_username_text() == f"{TemplateData.UPDATE_FIRST_NAME} {TemplateData.UPDATE_LAST_NAME}"

    @pytest.mark.usefixtures("login_home_logout")
    def test_register_login_and_change_password(self, login_home_logout):
        username, password, page = login_home_logout
        page = EditProfilePage(self.driver)
        page.nav_change_password_page()
        assert TestData.BASE_URL+Paths.CHANGE_PASSWORD == unquote(self.driver.current_url)
        page = ChangePasswordPage(self.driver)
        new_password = get_random_str()
        page.set_old_password(password)
        page.set_new_password(new_password)
        page.set_new_password_repeat(new_password)
        page.submit_change_password()
        assert page.is_success_presented()
        assert page.is_success_message_equal(SiteMessages.PASSWORD_CHANGED_SUCCESSFULLY)
        page = HomePage(self.driver, wait_for_logged_in_user=True)
        page.logout()
        page = LoginPage(self.driver)
        page.do_login(username, new_password)
        page = HomePage(self.driver, wait_for_logged_in_user=True)
        assert page.is_username_text_exists()





