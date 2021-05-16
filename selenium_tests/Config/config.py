from selenium_tests import ROOT_DIR
import os

class TestData:
    CHROME_EXECUTABLE_PATH = os.path.join(ROOT_DIR, os.path.join("Drivers/chromedriver_win32", "chromedriver.exe"))
    FIREFOX_EXECUTABLE_PATH = os.path.join(ROOT_DIR, os.path.join("Drivers/geckodriver_win64", "geckodriver.exe"))
    BASE_URL = "http://localhost:3000"
    TIMEOUT = 10
    REDUCED_TIMEOUT = 3
    N_REBALANCE_REFRESH = 10