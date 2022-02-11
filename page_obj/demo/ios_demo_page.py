import time
import os
from utils.driver import Driver
from utils.setting import DATA_DIR, run_device
# from basic_page.refresh_page import RefreshPage
from basic_page.base_page import SnapshotPage


# 测试用例配置文件路径
parent_catalogue = os.path.dirname(os.path.abspath(__file__)).split(os.sep)[-1]
CASE_DATA_YML = os.path.join(DATA_DIR, parent_catalogue, 'ios_demo.yml')
LOGIN_DATA_YML = os.path.join(DATA_DIR, parent_catalogue, 'login.yml')


class IosDemo(SnapshotPage):
    def start_app_dlg(self):
        """启动app弹框"""
        # login_data = YamlUtil(DATA_LOGIN_PATH).get_data()
        # find_type, ele = get_find_type_element(login_data, 'get_pos_dlg')
        # self.click(self.by(find_type, ele))

        # self.get_element(LOGIN_DATA_YML, 'get_pos_dlg').click()

        # find_type, ele = get_find_type_element(login_data, 'allow_news_dlg')
        # self.click(self.by(find_type, ele))

        # self.get_element(LOGIN_DATA_YML, 'allow_news_dlg').click()

        # find_type, ele = get_find_type_element(login_data, 'user_protocol_dlg')
        # self.click(self.by(find_type, ele))

        self.get_element(LOGIN_DATA_YML, 'user_protocol_dlg').click()
        self.get_element(LOGIN_DATA_YML, 'allow_news_dlg').click()


    def swipe_confirm(self, completed):
        """
        :param completed: 是否完成滑动function
        """
        # 写死，若滑动结束位置的横坐标每次变化较大，则不适用
        # 滑动按钮坐标
        btn_pos = [99, 460]
        # 滑动结束的位置
        end_pos = [280, 460]
        # 变化范围,变化位置不大，给了11的范围，可适当调整
        range_pos = [0, 11, -11]
        state = False
        for n in range(8):
            # 滑动三次
            for i in range(3):
                # print(f"第{i+1}次滑动")
                toX = 280 + range_pos[i]
                self.driver.execute_script('mobile: dragFromToForDuration',
                                           {
                                               "duration": 0.5,
                                               "element": None,
                                               'fromX': btn_pos[0],
                                               'fromY': btn_pos[1],
                                               "toX": toX,
                                               "toY": end_pos[1]
                                           })
                if completed():
                    state = True
                    break
            if state:
                break
        #
        return state

    # 是否完成滑动
    def complete_swipe(self):
        """是否完成滑动"""
        completed = True
        try:
            # self.find(*get_data(DATA_LOGIN_PATH, 'confirm_pic_loc'))
            self.get_element(LOGIN_DATA_YML, 'confirm_pic_loc')
            completed = False
        except:
            pass
        return completed

    def get_confirm_code(self):
        from PIL import Image
        img = Image.open('confirm_code.png')
        # 灰度转换
        image = img.convert('L')
        # 二值化
        pixels = image.load()
        for x in range(image.width):
            for y in range(image.height):
                if pixels[x, y] > 127.5:
                    pixels[x, y] = 255
                else:
                    pixels[x, y] = 0
        import re
        import pytesseract
        def change_Image_to_text(img):
            '''
            如果出现找不到训练库的位置, 需要我们手动自动
            语法: tessdata_dir_config = '--tessdata-dir "<replace_with_your_tessdata_dir_path>"'
            '''
            # testdata_dir_config = '--tessdata-dir "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata"'
            testdata_dir_config = '--tessdata-dir "/Users/qimeinian/Documents/qmn_application/Tesseract-ocr"'
            textCode = pytesseract.image_to_string(img, lang='eng', config=testdata_dir_config)
            # 去掉非法字符，只保留字母数字
            textCode = re.sub("\W", "", textCode)
            return textCode

    def login(self, account=None, pw=None):
        """登陆"""
        # 启动时权限、定位、用户协议弹框
        self.start_app_dlg()
        time.sleep(3)
        account = '18323721334'
        pw = 'Qmn123456'
        # 不指定账户时，默认读取配置文件
        if not (account and pw):
            # account = get_data(DATA_ACCOUNT_PATH, 'user', False)
            # pw = get_data(DATA_ACCOUNT_PATH, 'pw', False)
            account = '18323721334'
            pw = 'Qmn12345'
        else:
            pass
        # self.send_keys(get_data(DATA_LOGIN_PATH, 'account_loc'), account)
        # self.send_keys(get_data(DATA_LOGIN_PATH, 'passwd_loc'), pw)
        # self.click(get_data(DATA_LOGIN_PATH, 'login_btn_loc'))
        self.get_element(LOGIN_DATA_YML, 'account_loc').send_keys(account)
        self.get_element(LOGIN_DATA_YML, 'passwd_loc').send_keys(account)
        self.get_element(LOGIN_DATA_YML, 'login_protocol_loc').click()
        self.get_element(LOGIN_DATA_YML, 'login_btn_loc').click()

        time.sleep(2)
        # self.swipe_confirm(self.complete_swipe)
        self.get_element(LOGIN_DATA_YML, 'confirm_code_pic').screenshot('confirm_code.png')
        time.sleep(1.5)
        # 用户引导：点击查看全部应用
        # self.click(get_data(DATA_LOGIN_PATH, 'user_guide_dlg'))

    def check_body(self):
        # self.login()

        # self.get_element(LOGIN_DATA_YML, 'user_protocol_dlg').click()
        # self.get_element(LOGIN_DATA_YML, 'allow_news_dlg').click()
        # self.get_element(LOGIN_DATA_YML, 'account_loc').send_keys(account)
        # self.get_element(LOGIN_DATA_YML, 'passwd_loc').send_keys(account)
        # self.get_element(LOGIN_DATA_YML, 'login_protocol_loc').click()
        # self.get_element(LOGIN_DATA_YML, 'login_btn_loc').click()
        self.sort_operation(LOGIN_DATA_YML, 'user_protocol_dlg', 'click')
        time.sleep(6)
        self.sort_operation(LOGIN_DATA_YML, 'allow_news_dlg', 'click')
        time.sleep(2)
        self.sort_operation(LOGIN_DATA_YML, 'account_loc', 'send_keys', value='18323721334')
        time.sleep(2)
        self.sort_operation(LOGIN_DATA_YML, 'passwd_loc', 'send_keys', value='Qmn12345')
        time.sleep(2)
        self.sort_operation(LOGIN_DATA_YML, 'welcome_dmall_os', 'click')
        time.sleep(2)
        self.sort_operation(LOGIN_DATA_YML, 'login_protocol_loc', 'click')
        time.sleep(2)
        self.sort_operation(LOGIN_DATA_YML, 'login_btn_loc', 'click')


        # # time.sleep(3)
        # self.sort_operation(CASE_DATA_YML, 'search', 'click')
        # time.sleep(1)
        # self.sort_operation(CASE_DATA_YML, 'input', 'send_keys', value='帮助')
        # time.sleep(1)
        # self.sort_operation(CASE_DATA_YML, 'cancel', 'click')
        # time.sleep(1)
        # self.sort_operation(CASE_DATA_YML, 'news', 'click')
        # time.sleep(1)
        # self.sort_operation(CASE_DATA_YML, 'task', 'click')
        # time.sleep(1)
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
