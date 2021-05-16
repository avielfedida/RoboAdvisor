import time

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from selenium_tests.Config.config import TestData


class BasePage:

    def __init__(self, driver):
        self.driver = driver

    def ok_on_alert(self):
        WebDriverWait(self.driver, TestData.TIMEOUT).until(EC.alert_is_present())
        self.driver.switch_to.alert.accept()

    def wait_until_url_contains(self, partial):
        WebDriverWait(self.driver, TestData.TIMEOUT).until(EC.url_contains(partial))

    def send_text_to_draftjs(self, text):
        WebDriverWait(self.driver, TestData.TIMEOUT).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.notranslate.public-DraftEditor-content[role='textbox']"))).send_keys(text)

    def clean_local_storage(self):
        self.driver.execute_script('window.localStorage.clear();')

    def do_click(self, by_locator):
        WebDriverWait(self.driver, TestData.TIMEOUT).until(EC.visibility_of_element_located(by_locator)).click()

    def refresh_page(self):
        self.driver.refresh()

    def get_elements(self, by_locator):
        WebDriverWait(self.driver, TestData.TIMEOUT).until(EC.visibility_of_all_elements_located(by_locator))
        return self.driver.find_elements(*by_locator)

    def get_number_of_elements(self, by_locator):
        WebDriverWait(self.driver, TestData.TIMEOUT).until(EC.visibility_of_all_elements_located(by_locator))
        return len(self.driver.find_elements(*by_locator))

    def do_clear(self, by_locator):
        element = WebDriverWait(self.driver, TestData.TIMEOUT).until(EC.visibility_of_element_located(by_locator))
        element.send_keys(Keys.CONTROL, 'a')
        element.send_keys(Keys.DELETE)
        while len(element.get_attribute('value')) > 0:
            pass

    def delete_alert(self):
        element = self.driver.find_element(By.XPATH, "//div[@role='alert']")
        if element:
            self.driver.execute_script("""
            let element = arguments[0];
            element.parentNode.removeChild(element);
            """, element)
            # WebDriverWait(self.driver, TestData.TIMEOUT).until(EC.invisibility_of_element_located("//div[@role='alert']"))

    def do_tabs(self, n=1):
        ActionChains(self.driver).send_keys(Keys.TAB * n).perform()

    def do_text_chain(self, text):
        ActionChains(self.driver).send_keys(text).perform()

    def do_send_keys(self, by_locator, text):
        WebDriverWait(self.driver, TestData.TIMEOUT).until(EC.visibility_of_element_located(by_locator)).send_keys(text)

    def get_element_text(self, by_locator):
        element = WebDriverWait(self.driver, TestData.TIMEOUT).until(EC.visibility_of_element_located(by_locator))
        return element.text

    def is_visible(self, by_locator, timeout=None):
        element = WebDriverWait(self.driver, TestData.TIMEOUT if timeout is None else timeout).until(EC.visibility_of_element_located(by_locator))
        return bool(element)

    def text_to_be_present_in_element(self, by_locator, text):
        return WebDriverWait(self.driver, TestData.TIMEOUT).until(EC.text_to_be_present_in_element(by_locator, text))

    def is_invisible(self, by_locator):
        element = WebDriverWait(self.driver, TestData.TIMEOUT).until(EC.invisibility_of_element_located(by_locator))
        return bool(element)

    def get_title(self, title):
        WebDriverWait(self.driver, TestData.TIMEOUT).until(EC.title_is(title))
        return self.driver.title
