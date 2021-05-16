import time
import urllib
from urllib.parse import unquote

import pytest

from selenium_tests.Config.config import TestData
from selenium_tests.Data.Paths import Paths
from selenium_tests.Data.TemplateData import TemplateData
from selenium_tests.Pages.ClusterPage import ClusterPage
from selenium_tests.Pages.ClustersPage import ClustersPage
from selenium_tests.Pages.HomePage import HomePage
from selenium_tests.Pages.LoginPage import LoginPage
from selenium_tests.Pages.NewPostPage import NewPostPage
from selenium_tests.Pages.PostPage import PostPage
from selenium_tests.Pages.RegisterPage import RegisterPage
from selenium_tests.utils import get_random_username_password, get_cluster_title_url, get_random_str


@pytest.mark.usefixtures("tear_up_down", "do_register_login")
class Test_UserCases:



    def test_forum_navigation_not_logged_in(self):
        page = ClustersPage(self.driver)
        first_cluster_title = page.get_first_cluster_title()
        page.click_first_cluster()
        assert unquote(self.driver.current_url) == TestData.BASE_URL + get_cluster_title_url(first_cluster_title)

        page = ClusterPage(self.driver, first_cluster_title)
        assert page.is_new_post_btn_exists()
        page.click_new_post_btn()

        # Not logged in, thus we should be redirected to the login page
        assert self.driver.current_url == TestData.BASE_URL + Paths.LOGIN


    @pytest.mark.usefixtures("login_home_logout")
    def test_forum_navigation_with_login(self, login_home_logout):
        username, password, page = login_home_logout
        page.navigate_to_forum()
        assert unquote(self.driver.current_url) == TestData.BASE_URL + Paths.FORUM
        page = ClustersPage(self.driver)
        first_cluster_title = page.get_first_cluster_title()
        page.click_first_cluster()
        assert unquote(self.driver.current_url) == TestData.BASE_URL + get_cluster_title_url(first_cluster_title)

        page = ClusterPage(self.driver, first_cluster_title)
        assert page.is_new_post_btn_exists()
        page.click_new_post_btn()
        assert unquote(self.driver.current_url) == TestData.BASE_URL + get_cluster_title_url(
            first_cluster_title, page=None, new_post=True)

    @pytest.mark.usefixtures("login_home_logout")
    def test_add_new_post_and_message_to_it(self, login_home_logout):
        username, password, page = login_home_logout
        page.navigate_to_forum()
        assert unquote(self.driver.current_url) == TestData.BASE_URL + Paths.FORUM
        page = ClustersPage(self.driver)
        first_cluster_title = page.get_first_cluster_title()
        page.click_first_cluster()
        page = ClusterPage(self.driver, first_cluster_title)
        number_of_posts = page.get_number_of_posts()
        assert number_of_posts > 0
        page.click_new_post_btn()
        page = NewPostPage(self.driver, get_cluster_title_url(first_cluster_title, page=None, new_post=True))
        assert page.is_new_post_title_field_exists()
        assert page.is_new_post_submit_btn_exists()
        assert page.is_new_post_content_field_container_exists()
        title, content = page.fill_random()
        page.click_new_post_submit_btn()
        page = ClusterPage(self.driver, first_cluster_title)
        first_subject_title = page.get_first_title()
        assert first_subject_title == title
        href = unquote(page.click_post_title_link_return_href(title))
        page = PostPage(self.driver, href.split(TestData.BASE_URL)[1])
        assert page.is_new_message_btn()
        new_content = get_random_str()
        page.submit_new_message(new_content)
        assert page.is_message_with_content_exists(new_content)
