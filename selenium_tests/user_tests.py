# import unittest
import time
from functools import reduce
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import uuid
import pytest
import pytest_html
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from time import sleep
import sys
import os

# '''
# py.test.exe --capture=no --verbose --html=C:\Users\aviel\Desktop\nginx_basic_server\services\nginx\html\report_test_register10.html test_register.py
# '''

# Fixture for Firefox
@pytest.fixture(params=["chrome", "firefox"], scope="class")
def driver_init(request):
    if request.param == "chrome":
        web_driver = webdriver.Chrome(executable_path=os.path.join("chromedriver_win32", "chromedriver.exe"))
    if request.param == "firefox":
        web_driver = webdriver.Firefox(executable_path=os.path.join("geckodriver_win64", "geckodriver.exe"))
    yield web_driver
    web_driver.close()
    web_driver.quit()


@pytest.fixture(scope="class")
def tear_up_down(request, driver_init):
    request.cls.driver = driver_init
    # must have chrome browser installed on machine and driver in this relative location
    request.cls.domain = "http://roboadv.westeurope.cloudapp.azure.com/"
    request.cls.timeout = 8
    yield
    # Nothing to do after for now


@pytest.mark.usefixtures("tear_up_down")
class Test_users_actions:

    def register_user(self):
        self.driver.find_element_by_id("nav_link_register").click()

        # Wait for registration form to be loaded
        WebDriverWait(self.driver, self.timeout).until(EC.presence_of_element_located((By.ID, 'register_screen')))

        email = self.driver.find_element_by_id("email_field")
        first_name = self.driver.find_element_by_id("first_name_field")
        last_name = self.driver.find_element_by_id("last_name_field")
        password = self.driver.find_element_by_id("password_field")
        password_repeat = self.driver.find_element_by_id("password_repeat_field")
        birth_date = self.driver.find_element_by_id("birth_date_field")

        email.send_keys(f'{str(uuid.uuid4())}@gmail.com')
        first_name.send_keys('אביאל')
        last_name.send_keys('פדידה')
        password.send_keys('123')
        password_repeat.send_keys('123')
        birth_date.send_keys('01/06/1994')

        self.driver.find_element_by_id("submit_btn").click()

        WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located((By.XPATH, "//span[@data-variant='success']")))

        success_message = self.driver.find_element_by_xpath("//span[@data-variant='success']")
        assert "המשתמש נרשם בהצלחה למערכת" == success_message.text


        return {"email": email.get_property('value'), "password": password.get_property('value'), "first_name": first_name.get_property('value'), "last_name": last_name.get_property('value')}

    def login_user(self, data):
        # Wait for registration form to be loaded
        self.driver.find_element_by_id("nav_link_login").click()
        WebDriverWait(self.driver, self.timeout).until(EC.presence_of_element_located((By.ID, 'login_screen')))
        self.driver.find_element_by_id("email_field").send_keys(data['email'])
        self.driver.find_element_by_id("password_field").send_keys(data['password'])
        self.driver.find_element_by_id("submit_btn").click()
        WebDriverWait(self.driver, self.timeout).until(EC.presence_of_element_located((By.ID, 'username')))
        username = self.driver.find_element_by_id("username")
        assert f"{data['first_name']} {data['last_name']}" == username.text

    def test_login_fail_then_register_then_login_success(self):
        # Open page
        self.driver.get(self.domain)

        # Register
        data = self.register_user()
        self.driver.back()

        # Login
        self.login_user(data)
        self.driver.back()

        # Edit first/last names

        sleep(2)

        #
        # # assert can be based on many things - url name, stating the username in html tags and more...
        # WebDriverWait(driver, 10).until(EC.url_to_be("https://www.saucedemo.com/inventory.html"))



