import pytest
from utils.myairtest import MyWebChrome
from utils.setting import DRIVER_PATH, DRIVER_SIZE
from selenium.webdriver.chrome.options import Options
from utils.mobileairtest import connect_android, start_yosemite
from utils.setting import run_device
from utils.driver import Driver

@pytest.fixture(scope='session')
def start_web():
    if run_device == 0:
        chrome_options = Options()
        driver = MyWebChrome(DRIVER_PATH, chrome_options=chrome_options)
        driver.set_window_size(*DRIVER_SIZE)
        driver.implicitly_wait(30)
        yield driver
        driver.quit()
    elif run_device == 1: #pad
        pass
    elif run_device == 2: #android_mobile
        driver_obj = Driver()
        driver = driver_obj.get()
        connect_android()
        start_yosemite()
        yield driver
        driver_obj.stop()
