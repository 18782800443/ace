import sys, os
import time
import pytest
from utils.myairtest import MyWebChrome
from utils.setting import DRIVER_PATH, DRIVER_SIZE, run_type
from selenium.webdriver.chrome.options import Options
from utils.mobileairtest import connect_android, start_yosemite
from utils.setting import run_device
from utils.driver import Driver

sys.path.append((os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))))


@pytest.fixture(scope='session')
def start_web():
    # web
    if run_device == 0:
        chrome_options = Options()
        driver = MyWebChrome(DRIVER_PATH, chrome_options=chrome_options)
        driver.set_window_size(*DRIVER_SIZE)
        driver.implicitly_wait(30)
        yield driver
        driver.quit()
    # pad
    elif run_device == 1:
        pass
    # android_mobile
    elif run_device == 2:
        driver_obj = Driver()
        driver = driver_obj.get()
        connect_android()
        start_yosemite()
        yield driver
        driver_obj.stop()
    elif run_device == 3:
        from utils.mobileairtest import kill_ios_iproxy, connect_ios
        kill_ios_iproxy()
        driver = Driver()
        # 通过图像执行，调用airtest API，需要先连接设备
        if run_type == 2:
            connect_ios()
        time.sleep(3)
        yield driver.get()
        driver.stop()
