import unittest
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import uuid

class LoginTests(unittest.TestCase):
    def setUp(self):
        # must have chrome browser installed on machine and driver in this relative location
        self.driver = webdriver.Chrome(executable_path='chromedriver_win32/chromedriver.exe')
        self.domain = "http://localhost:3000/"
        self.timeout = 3


    def register_user(self):


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
        return {"email": email.get_property('value'), "password": password.get_property('value'), "first_name": first_name.get_property('value'), "last_name": last_name.get_property('value')}

    def login_user(self, email, password):
        # Wait for registration form to be loaded
        WebDriverWait(self.driver, self.timeout).until(EC.presence_of_element_located((By.ID, 'login_screen')))
        self.driver.find_element_by_id("email_field").send_keys(email)
        self.driver.find_element_by_id("password_field").send_keys(password)
        self.driver.find_element_by_id("submit_btn").click()

    def test_login_fail_then_register_then_login_success(self):
        # Open page
        self.driver.get(self.domain)

        # Navigate to login page
        self.driver.find_element_by_id("nav_link_login").click()
        self.login_user(f'{str(uuid.uuid4())}@gmail.com', "123")
        WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located((By.XPATH, "//span[@data-variant='danger']")))
        danger_message = self.driver.find_element_by_xpath("//span[@data-variant='danger']")
        self.assertEqual("שם משתמש/סיסמה לא נמצאו", danger_message.text)


        # Navigate to register page
        self.driver.find_element_by_id("nav_link_register").click()
        data = self.register_user()
        # Wait for server response
        WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located((By.XPATH, "//span[@data-variant='success']")))

        success_message = self.driver.find_element_by_xpath("//span[@data-variant='success']")
        self.assertEqual("המשתמש נרשם בהצלחה למערכת", success_message.text)


        # Navigate to login page
        self.driver.find_element_by_id("nav_link_login").click()
        self.login_user(data['email'], data['password'])
        WebDriverWait(self.driver, self.timeout).until(EC.presence_of_element_located((By.ID, 'username')))
        username = self.driver.find_element_by_id("username")
        self.assertEqual(f"{data['first_name']} {data['last_name']}", username.text)

        sleep(2)

        #
        # # assert can be based on many things - url name, stating the username in html tags and more...
        # WebDriverWait(driver, 10).until(EC.url_to_be("https://www.saucedemo.com/inventory.html"))

    def tearDown(self):
        self.driver.close() # Close tab/window
        self.driver.quit() # Close driver


if __name__ == "__main__":
    unittest.main()
