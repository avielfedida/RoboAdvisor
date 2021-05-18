import pytest
from selenium import webdriver

from selenium_tests.Config.config import TestData
# @pytest.fixture(params=["chrome", "firefox"], scope="class")
from selenium_tests.Data.TemplateData import TemplateData
from selenium_tests.Pages.HomePage import HomePage
from selenium_tests.Pages.LoginPage import LoginPage
from selenium_tests.Pages.RegisterPage import RegisterPage
from selenium_tests.utils import get_random_username_password, get_driver_in_self


@pytest.fixture(params=["chrome"], scope="session")
def init_driver(request):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    if request.param == "chrome":
        web_driver = webdriver.Chrome(executable_path=TestData.CHROME_EXECUTABLE_PATH, options=options)
    if request.param == "firefox":
        web_driver = webdriver.Firefox(executable_path=TestData.FIREFOX_EXECUTABLE_PATH, options=options)
    yield web_driver
    web_driver.close()
    web_driver.quit()


def ext_do_register_login(self):
    page = RegisterPage(self.driver)
    username, password = get_random_username_password()
    page.do_register(username=username, password=password, birth_date=TemplateData.BIRTH_DATE,
                     first_name=TemplateData.FIRST_NAME, last_name=TemplateData.LAST_NAME)
    page = LoginPage(self.driver)
    page.do_login(username, password)
    return username, password


@pytest.fixture(scope="class")
def do_register_login(request):
    request.cls.do_register_login = ext_do_register_login
    yield
    pass


@pytest.fixture(scope="function")
def login_home_logout(init_driver):
    self = get_driver_in_self(init_driver)
    username, password = ext_do_register_login(self)
    page = HomePage(self.driver, wait_for_logged_in_user=True)
    yield username, password, page
    page = HomePage(self.driver, wait_for_logged_in_user=True)
    page.logout()


@pytest.fixture(scope="class")
def tear_up_down(request, init_driver):
    request.cls.driver = init_driver
    # must have chrome browser installed on machine and driver in this relative location
    request.cls.timeout = TestData.TIMEOUT
    yield
    # Nothing for now
