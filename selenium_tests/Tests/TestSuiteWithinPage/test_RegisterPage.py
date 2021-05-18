import pytest

from selenium_tests.Data.SiteMessages import SiteMessages
from selenium_tests.Data.TemplateData import TemplateData
from selenium_tests.Pages.RegisterPage import RegisterPage
from selenium_tests.utils import get_random_username_password


@pytest.mark.usefixtures("tear_up_down")
class Test_RegisterPage:

    def test_crucial_elements_visibility(self):
        page = RegisterPage(self.driver)
        assert page.is_register_btn_exists()
        assert page.is_email_field_exists()
        assert page.is_password_field_exists()
        assert page.is_password_repeat_field_exists()
        assert page.is_first_name_field_exists()
        assert page.is_last_name_field_exists()
        assert page.is_birth_date_field_exists()

    def test_register_fail(self):
        username, password = get_random_username_password()

        page = RegisterPage(self.driver)

        page.refresh_page()
        assert page.is_danger_not_presented()
        page.do_register(username="", password=password, birth_date=TemplateData.BIRTH_DATE,
                         first_name=TemplateData.FIRST_NAME, last_name=TemplateData.LAST_NAME)
        assert page.is_danger_presented()

        page.refresh_page()
        assert page.is_danger_not_presented()
        page.do_register(username=username, password="", birth_date=TemplateData.BIRTH_DATE,
                         first_name=TemplateData.FIRST_NAME, last_name=TemplateData.LAST_NAME)
        assert page.is_danger_presented()

        page.refresh_page()
        assert page.is_danger_not_presented()
        page.do_register(username=username, password=password, birth_date="", first_name=TemplateData.FIRST_NAME,
                         last_name=TemplateData.LAST_NAME)
        assert page.is_danger_presented()

        page.refresh_page()
        assert page.is_danger_not_presented()
        page.do_register(username=username, password=password, birth_date=TemplateData.BIRTH_DATE, first_name="",
                         last_name=TemplateData.LAST_NAME)
        assert page.is_danger_presented()

        page.refresh_page()
        assert page.is_danger_not_presented()
        page.do_register(username=username, password=password, birth_date=TemplateData.BIRTH_DATE,
                         first_name=TemplateData.FIRST_NAME, last_name="")
        assert page.is_danger_presented()

    def test_register_twice_same_username(self):
        page = RegisterPage(self.driver)
        username, password = get_random_username_password()
        page.do_register(username=username, password=password, birth_date=TemplateData.BIRTH_DATE,
                         first_name=TemplateData.FIRST_NAME, last_name=TemplateData.LAST_NAME)
        assert page.is_success_presented()
        assert page.is_success_message_equal(SiteMessages.REGISTER_SUCCESSFULLY)
        page.refresh_page()
        page.do_register(username=username, password=password, birth_date=TemplateData.BIRTH_DATE,
                         first_name=TemplateData.FIRST_NAME, last_name=TemplateData.LAST_NAME)
        assert page.is_danger_presented()
        assert page.is_danger_message_equal(SiteMessages.REGISTER_ALREADY_USER_EXISTS)


    def test_register_success(self):
        page = RegisterPage(self.driver)
        username, password = get_random_username_password()
        page.do_register(username=username, password=password, birth_date=TemplateData.BIRTH_DATE,
                         first_name=TemplateData.FIRST_NAME, last_name=TemplateData.LAST_NAME)
        assert page.is_success_presented()
        assert page.is_success_message_equal(SiteMessages.REGISTER_SUCCESSFULLY)
