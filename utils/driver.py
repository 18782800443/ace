import os
import time
from appium import webdriver
from utils.setting import CONF_DIR
from utils.yaml_util import YamlUtil
from utils.log_util import LogUtil

logger = LogUtil().get()


class Driver:
    def __init__(self):
        yaml_path = os.path.join(CONF_DIR, "desire_cap.yml")
        appium_address = os.path.join(CONF_DIR, 'appium_address.yml')
        yaml_util = YamlUtil(yaml_path)
        self.desired_caps = yaml_util.get_data()
        self.desired_caps['noReset'] = True
        self.desired_caps['fullReset'] = False
        self.address_yaml = YamlUtil(appium_address).get_data()
        self.driver = webdriver.Remote(self.address_yaml["address"], self.desired_caps)

    def get(self):
        try:
            driver = self.driver
            logger.success("连接设备成功")
            return driver
        except Exception as e:
            logger.error("连接设备失败")
            raise e

    def stop(self):
        time.sleep(2)
        self.driver.quit()
        logger.success("关闭设备连接成功")


if __name__ == '__main__':
    driver = Driver()

