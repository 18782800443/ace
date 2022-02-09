import time
import os
from utils.driver import Driver
from utils.setting import DATA_DIR, run_device
# from basic_page.refresh_page import RefreshPage
from basic_page.base_page import SnapshotPage


# 测试用例配置文件路径
parent_catalogue = os.path.dirname(os.path.abspath(__file__)).split(os.sep)[-1]
CASE_DATA_YML = os.path.join(DATA_DIR, parent_catalogue, 'ios_demo.yml')


class IosDemo(SnapshotPage):
    def check_body(self):
        # time.sleep(3)
        self.sort_operation(CASE_DATA_YML, 'search', 'click')
        time.sleep(2)
        self.sort_operation(CASE_DATA_YML, 'input', 'send_keys', value='帮助')
        time.sleep(2)
        self.sort_operation(CASE_DATA_YML, 'cancel', 'click')
        time.sleep(2)
        # self.sort_operation(CASE_DATA_YML, 'news', 'click')
        # time.sleep(2)
        # self.sort_operation(CASE_DATA_YML, 'task', 'click')
        # time.sleep(2)
        # self.sort_operation(CASE_DATA_YML, 'item_task', 'wait_element_visibility')


# if __name__ == '__main__':
    # 测试截图
    # driver = Driver().get()
    # time.sleep(3)
    # driver.get_screenshot_as_file('home.png')
    # data = driver.get_screenshot_as_base64()
    # print(data)
    # import numpy as np
    # import cv2
    # # def string_2_img(pngstr):
    # #     nparr = np.frombuffer(pngstr, np.uint8)
    # #     img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    # #     return img
    # # screen = string_2_img(data)
    # # cv2.imwrite('screen.png', data)
    # import base64
    # imgdata = base64.b64decode(data)
    # with open('screen.png', 'wb') as fw:
    #     fw.write(imgdata)

if __name__ == '__main__':
    from utils.setting import run_type
    from utils.mobileairtest import connect_ios, start_ios_app, kill_ios_iproxy
    kill_ios_iproxy()
    driver = Driver().get()
    # # time.sleep(3)
    # # start_ios_app()
    demo = IosDemo(driver)
    # time.sleep(3)
    if run_type == 2:
        connect_ios()
    demo.check_body()
