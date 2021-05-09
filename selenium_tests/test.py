import unittest
from time import sleep

from selenium_tests import webdriver
from selenium_tests.webdriver.common.by import By
from selenium_tests.webdriver.support.wait import WebDriverWait
from selenium_tests.webdriver.support import expected_conditions as EC


class LoginTests(unittest.TestCase):
    """
    in order to build good selenium test try to enter the website manually and inspect it's html elements.
    also with the ctrl + shift + C to inspect specific elements

    if you want that the test will run slowly and see actions - use sleep in
    different places

    """

    def setUp(self):
        # must have chrome browser installed on machine and driver in this relative location
        self.driver = webdriver.Chrome(executable_path='chromedriver_win32/chromedriver.exe')

    def test_success_login(self):
        driver = self.driver
        driver.get("https://www.saucedemo.com/")

        username = driver.find_element_by_name("user-name")
        password = driver.find_element_by_name("password")

        username.send_keys('standard_user')
        password.send_keys('secret_sauce')

        driver.find_element_by_id("login-button").click()

        # assert can be based on many things - url name, stating the username in html tags and more...
        WebDriverWait(driver, 10).until(EC.url_to_be("https://www.saucedemo.com/inventory.html"))

    def test_fail_login(self):
        driver = self.driver
        driver.get("https://www.saucedemo.com/")

        # find element by id
        username = driver.find_element_by_id("user-name")
        password = driver.find_element_by_id("password")

        username.send_keys('standard_user')
        password.send_keys('blabla')

        driver.find_element_by_id("login-button").click()

        # assert can be based on many things - url name, stating the username in html tags and more...
        WebDriverWait(driver, 10).until(EC.url_to_be("https://www.saucedemo.com/"))

    def test_fail_login_assert_message(self):
        driver = self.driver
        driver.get("https://www.saucedemo.com/")

        username = driver.find_element_by_id("user-name")
        password = driver.find_element_by_id("password")

        username.send_keys('standard_user')
        password.send_keys('blabla')

        driver.find_element_by_id("login-button").click()

        WebDriverWait(driver, 10).until(EC.url_to_be("https://www.saucedemo.com/"))

        # timeout for login try
        error_container = WebDriverWait(driver, 10).\
            until(EC.presence_of_element_located((By.CLASS_NAME, 'error-message-container')))

        # get the text of the first h3 element inside error container
        error_text = error_container.find_element_by_xpath("//h3[1]").text
        assert error_text == "Epic sadface: Username and password do not match any user in this service"


    def test_logout(self):
        driver = self.driver
        driver.get("https://www.saucedemo.com/")

        username = driver.find_element_by_name("user-name")
        password = driver.find_element_by_name("password")

        username.send_keys('standard_user')
        password.send_keys('secret_sauce')

        driver.find_element_by_id("login-button").click()

        sleep(3)

        WebDriverWait(driver, 10).until(EC.url_to_be("https://www.saucedemo.com/inventory.html"))

        # timeout for menu button to appear
        menu = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'react-burger-menu-btn')))

        # click on menu button
        menu.click()

        sleep(3)

        # timeout for logout button
        logout = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'logout_sidebar_link')))

        # because logout is not a button we must click it this way
        driver.execute_script("arguments[0].click();", logout)

        sleep(3)

        # assert we are back to home page
        WebDriverWait(driver, 10).until(EC.url_to_be("https://www.saucedemo.com/"))

        # we can assert more things here if needed, like appearance of login form

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
