import cv2
# import win32api
# import win32con
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import datetime
import allure
from utils.yaml_util import YamlUtil
from utils.setting import *
import re
import numpy as np
from utils.setting import run_type
from utils.util import get_pic_name
from utils.util import logger
from selenium.webdriver import ActionChains
from airtest.core.api import *
from utils.mobileairtest import input_value


TEMPLATE_WEB = {
    'click': 'airtest_touch',
    'wait_element_visibility': 'assert_template',
    'send_keys': 'input_value',
    'move_to_gap': 'drag_and_move',
    "find": "assert_template",
}

TEMPLATE_PHONE = {
    "click": "touch",
    "wait_element_visibility": "wait",
    "send_keys": "input_value",
    "swipe_action": "swipe",
    "find": "exists",
}

TEMPLATE = TEMPLATE_WEB if run_device == 0 else TEMPLATE_PHONE


class BasePage(object):

    def __init__(self, driver):
        self.logger = logger
        self.driver = driver

    def wait_element_visibility(self, locator, timeout=10, poll_frequency=0.1):
        """
        等待元素可见
        :param locator: 定位表达式
        :param timeout: 等待超时时间
        :param poll_frequency: 查询元素时间间隔
        :return:
        """
        # 等待元素之前获取当前的时间
        start_time = time.time()
        try:
            ele = WebDriverWait(self.driver, timeout, poll_frequency).until(
                EC.visibility_of_element_located(locator)
            )
        except Exception as e:
            import traceback
            traceback.print_exc()
            # 输出日志
            logger.error("元素 {} 等待可见超时", locator)
            # 对当前页面进行截图
            screen_shot = self.get_screen()
            self.upload_allure_screen()
            logger.info('已截图，路径：{}', screen_shot)
            raise e
        else:
            # 元素等待出现之后，获取实际
            end_time = time.time()
            logger.info("元素 {} 可见,等待时间{}秒", locator, end_time - start_time)
            return ele

    def find(self, *loc):
        """
        重写查找单个元素方法,如果定位不到先检查是否因为出现弹窗
        """
        try:
            self.wait_element_visibility(loc)
            return self.driver.find_element(*loc)
        except AttributeError:
            if self.is_toast_exist():
                self.find(*loc).click()
            else:
                self.upload_allure_screen()

    def find_elements(self, *loc):
        """
        重写查找多个元素方法
        """
        try:
            self.wait_element_visibility(loc)
            return self.driver.find_elements(*loc)
        except AttributeError:
            if self.is_toast_exist():
                self.find_elements(*loc).click()
            else:
                self.upload_allure_screen()

    @staticmethod
    def by(find_type, element):
        """
        重写by方法
        """
        if find_type.lower() == "id":
            ele = (By.ID, element)
            return ele
        if find_type.lower() == "xpath":
            ele = (By.XPATH, element)
            return ele
        if find_type.lower() == "selector_text":
            element = f'new UiSelector().text("{element}")'
            ele = (By.ANDROID_UIAUTOMATOR, element)
            return ele

    def click(self, loc):
        """
        重写点击元素方法
        """
        try:
            self.find(*loc).click()
        except Exception as e:
            logger.error("点击元素{}失败", loc)
            screen_shot = self.get_screen()
            self.upload_allure_screen()
            logger.info('已截图，路径：{}', screen_shot)
            raise e

    def send_keys(self, loc, value, clear_first=True, click_first=True):
        """
        重写send_keys方法
        """
        try:
            # loc = getattr(self, "_%s" % loc)  # getattr相当于实现self.loc
            ele = self.find(*loc)
            if click_first:
                ele.click()
            if clear_first:
                ele.clear()
                ele.send_keys(value)
        except AttributeError:
            logger.error('未找到元素：{} 请检查！', loc[1])
            screen_shot = self.get_screen()
            self.upload_allure_screen()
            logger.info('已截图，路径：{}', screen_shot)

    def is_toast_exist(self):
        """is toast exist, return True or False
        :Agrs:
            - text   - 对于可能出现的弹窗关键字配置到toast.yml文件中
        :Usage:
            is_toast_exist("判断弹窗是否存在")
        """
        text=""
        try:
            toast_list = self.get_toast()
            logger.info(toast_list)
            for text in toast_list:
                toast_loc = (By.XPATH, ".//*[contains(@text,'%s')]" % text)
                try:
                    self.wait_element_visibility(toast_loc)
                    return True
                except Exception as e:
                    pass
                    logger.warn('未找到弹窗元素：{} 请检查！', text)
            return False
        except Exception as e:
            logger.error('未找到弹窗元素：{} 请检查！', text)
            screen_shot = self.get_screen()
            logger.info('已截图，路径：{}', screen_shot)
            return False

    def is_element_exist(self, *loc):
        """
        查看页面元素是否存在
        """
        try:
            self.wait_element_visibility(loc)
            self.driver.find_element(*loc)
            return True
        except Exception:
            logger.error(f'未找到元素：{loc} 请检查！')
            screen_shot = self.get_screen()
            logger.info('已截图，路径: {}', screen_shot)
            return False

    def get_size(self):
        """
        获取屏幕大小
        """
        try:
            size = self.driver.get_window_size()
            return size
        except Exception:
            logger.error('获取屏幕尺寸失败')
            return None

    def get_screen(self, screen_img):
        """
                获取屏幕截图
                :Args:
                 - scree_path: 如片保存地址
                """
        now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        if not os.path.exists(ERROR_IMG):
            os.makedirs(ERROR_IMG)
        screen_img = os.path.join(ERROR_IMG, screen_img) if screen_img else os.path.join(ERROR_IMG, now + '.png')
        self.driver.get_screenshot_as_file(screen_img)
        return screen_img


    def upload_allure_screen(self):
        """
        截图显示在allure的测试报告中
        """
        now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        allure.attach(self.driver.get_screenshot_as_png(), now + '.png', attachment_type=allure.attachment_type.PNG)

    def upload_allure_pic(self, pic_path, pic_name):
        """
        显示指定图片到allure的测试报告中
        """
        with open(pic_path, 'rb') as f:
            pic = f.read()
            allure.attach(pic, pic_name, attachment_type=allure.attachment_type.PNG)

    def get_toast(self):
        """
        获取配置文件中存在的元素
        """
        toast_path = os.path.join(CONF_DIR, "toast.yml")
        toast_list = YamlUtil(toast_path).get_data().values()
        return toast_list

    def get_mobile_log(self):
        """
        使用该方法后，手机端 logcat 缓存会清除归零，从新记录
        建议每条用例执行完执行一边清理，遇到错误再保存减少陈余 log 输出
        Android
        """
        logcat = self.driver.get_log('logcat')
        c = '\n'.join([i['message'] for i in logcat])
        allure.attach(c, 'MobileLog', allure.attachment_type.TEXT)
        # 写入到 allure 测试报告中

    def swipe_action(self, direction, num):
        """
        :param direction: 反向，向左，右，上，下
        :param num: 控制次数，为了防止在前面出现这种循环，因此在基础类中添加
        :return:
        """
        size = self.get_size()
        x_value = size["width"]
        y_value = size["height"]
        for i in range(num):
            try:
                if direction == 'up':
                    self.driver.swipe(x_value * 0.5, y_value * 0.7, x_value * 0.5, y_value * 0.3)
                if direction == 'down':
                    self.driver.swipe(x_value * 0.5, y_value * 0.1, x_value * 0.5, y_value * 0.9)
                if direction == 'right':
                    self.driver.swipe(x_value * 0.9, y_value * 0.5, x_value * 0.1, y_value * 0.5)
                if direction == 'left':
                    self.driver.swipe(x_value * 0.1, y_value * 0.5, x_value * 0.9, y_value * 0.5)
            except Exception as e:
                # 输出日志
                logger.error("第{}次滑动--失败", i + 1)
                # 对当前页面进行截图
                self.get_screen()
                raise e
            else:
                pass
                logger.info("第{}次滑动--成功", i + 1)


    def move_to_gap(self, loc, position):
        """
        拖动滑块到缺口处
        :param slider:滑块
        :param 偏移量:轨迹
        :return:
        """
        action = ActionChains(self.driver)
        ele = self.find(*loc)
        x, y = position
        action.click_and_hold(ele).perform()
        action.move_by_offset(xoffset=5, yoffset=5).perform()
        # action.move_by_offset(xoffset=5, yoffset=5).perform()
        action.move_by_offset(xoffset=x-5, yoffset=y-5).perform()
        action.reset_actions()
        time.sleep(0.5)


class SnapshotPage(BasePage):

    def sort_operation(self, *args, **kwargs):
        """
        根据全局参数run_type，判断指定用例方式:：1、selenium或者appium的xpath操作 2、通过xpath操作，并截图 3、通过图像识别定位操作
        """
        if run_type == 0:
            self.operation_element(*args, **kwargs)
        elif run_type == 1:
            self.element_snapshot(*args, **kwargs)
            self.operation_element(*args, **kwargs)
        elif run_type == 2:
            self.operation_pic(*args, **kwargs)

    def operation_pic(self, case_data_yml, element_loc, method_str='click', **kwargs):
        """
        通过操作图片方式运行用例
        """
        data = self.get_loc_data(case_data_yml, element_loc)
        if data.get('image', None):
            self.run_pic_yml(case_data_yml, data, method_str=method_str, **kwargs)
        else:
            # ------------------iOS------------------
            # 针对iOS，根据设备名称区分，而不根据端区分；
            if run_device == 3:
                device_name = YamlUtil(os.path.join(CONF_DIR, 'desire_cap.yml')).get_data().get('name', 'ios')
                pic_path = get_pic_name(os.path.join(os.path.dirname(case_data_yml), device_name), element_loc)
                method_str = TEMPLATE_PHONE[method_str]
                v = self.get_template(pic_path)
                self.run_variety_device(v, method_str, **kwargs)
                return
            # ------------------iOS------------------
            pic_path = get_pic_name(self.get_pic_dirpath(case_data_yml), element_loc)
            method_str = TEMPLATE[method_str]
            v = self.get_template(pic_path)
            self.run_variety_device(v, method_str, **kwargs)

    def run_pic_yml(self, case_data_yml, data, method_str='click', **kwargs):
        """
        针对yml文件中就有图片的情况
        """
        pic_dirpath = self.get_pic_dirpath(case_data_yml)
        pic_path = os.path.join(pic_dirpath, data['image'])
        v = self.get_template(pic_path, resolution=data.get('resolution', None), target_pos=data.get('target_pos', None))
        try:
            self.run_variety_device(v, method_str, **kwargs)
        except AttributeError:
            self.run_variety_device(v, TEMPLATE[method_str], **kwargs)

    def run_variety_device(self, v, method_str, **kwargs):
        """
        不同设备、系统用不通的图片对比方式
        """
        if run_device == 0:
            self.oper_pic_web(v, method_str, **kwargs)
        elif run_device == 1:
            pass
        elif run_device == 2:
            self.oper_pic_device(v, method_str, **kwargs)
        # ------------------iOS------------------
        elif run_device == 3:
            self.oper_pic_device(v, method_str, **kwargs)
        # ------------------iOS------------------

    def get_pic_dirpath(self, case_data_yml):
        """
        根据yml文件去找到对应的图片文件路径
        """
        device_name = YamlUtil(os.path.join(CONF_DIR, 'desire_cap.yml')).get_data()[
            'deviceName'] if run_device != 0 else "web"
        return os.path.join(os.path.dirname(case_data_yml), device_name)

    def get_template(self, pic_path, resolution=None, target_pos=None):
        """
        生成template对象
        """
        # ------------------iOS------------------
        if run_device == 3:
            return Template(pic_path, threshold=ST.THRESHOLD, rgb=False, resolution=(1242, 2208))
        # ------------------iOS------------------
        if not resolution:
            pic_name = os.path.basename(os.path.splitext(pic_path)[0])
            resolution = pic_name.split('_')[-1]
        target_pos = "5" if not target_pos else target_pos
        return Template(f'{pic_path}', threshold=ST.THRESHOLD, rgb=False, resolution=eval(resolution), target_pos=eval(target_pos))

    def oper_pic_web(self, v, method, **kwargs):
        """
        web端比较图片的方法
        """
        method = getattr(self.driver, method)
        method(v, **kwargs)

    def oper_pic_device(self, v, method, **kwargs):
        """
        app端比较图片的方法
        """
        from utils import mobileairtest
        method = getattr(mobileairtest, method)
        method(v, **kwargs)

    def operation_element(self, case_data_yml, element_loc, method_str='click',  **kwargs):
        """
        定位并操作元素
        """
        data = self.get_loc_data(case_data_yml, element_loc)
        if data.get('image', None):
            self.run_pic_yml(case_data_yml, data, method_str=method_str, **kwargs)
        else:
            # ------------------iOS------------------
            # 这里区分iOS是因为，iOS使用base_page中元素定位的方法会经常失败
            if run_device == 3:
                ele = self.get_element(case_data_yml, element_loc)
                if method_str in ['click']:
                    ele.click()
                elif method_str in ['send_keys']:
                    if kwargs.get('value') is not None:
                        ele.send_keys(kwargs.get('value'))
                elif method_str in ['wait_element_visibility', 'find', 'find_elements', 'is_element_exist']:
                    pass
                else:
                    raise Exception(f"The function {method_str} is not yet adapted")
                return
            # ------------------iOS------------------
            data = self.get_loc_data(case_data_yml, element_loc)
            frame_dict = self.is_switch_iframe(data)
            data = frame_dict if frame_dict else data
            find_type, element = data['find_type'], data['element']
            loc = self.by(find_type, element)
            method = getattr(self, method_str)
            if method_str in ['click', 'wait_element_visibility']:
                res = method(loc)
            elif method_str in ['find', 'find_elements', 'is_element_exist']:
                res = method(*loc)
            elif method_str in ['send_keys', 'move_to_gap']:
                res = method(loc, **kwargs)
            else:
                raise Exception(f"The function {method_str} is not yet adapted")
            if frame_dict:
                self.driver.switch_to.default_content()
            return res

    def is_switch_iframe(self, data):
        frame_dict = data.get("frame", None)
        if frame_dict:
            frame_find_type = data['find_type']
            frame_element = data['element']
            self.frame_ele = self.find(*self.by(frame_find_type, frame_element))
            frame_dict['location'] = self.frame_ele.location
            frame_name = frame_dict['name']
            self.driver.switch_to.frame(frame_name)
            return frame_dict

    def get_element_location(self, data_path, loc_str):
        """
        解析yml元素文件
        """
        data = self.get_loc_data(data_path, loc_str)
        frame_dict = self.is_switch_iframe(data)
        element_str = frame_dict if frame_dict else data
        # ------------------iOS------------------
        # iOS单独使用定位方法，不使用base_page中的
        if run_device == 3:
            ele = self.get_element(data_path, loc_str)
        # ------------------iOS------------------
        else:
            ele = self.find(*self.by(element_str['find_type'], element_str['element']))
        if frame_dict:
            x = ele.location['x'] + frame_dict['location']['x']
            y = ele.location['y'] + frame_dict['location']['y']
            ele_location = {'x': x, "y": y}
            ele_size = ele.size
            self.driver.switch_to.default_content()

        else:
            ele_location = ele.location
            ele_size = ele.size
        return ele_location, ele_size

    # 主要针对iOS
    def get_element(self, data_path, loc_str):
        """
        定位元素
        """
        data = self.get_loc_data(data_path, loc_str)
        frame_dict = self.is_switch_iframe(data)
        element_str = frame_dict if frame_dict else data
        # ele = self.find(*self.by(element_str['find_type'], element_str['element']))
        print(element_str['find_type'], element_str['element'])
        if element_str['find_type'] == 'ios_predicate':
            ele = self.driver.find_element_by_ios_predicate(element_str['element'])
        elif element_str['find_type'] == 'xpath':
            ele = self.driver.find_element_by_xpath(element_str['element'])
        return ele

    def get_ele_bounds(self, ele):
        """
        获取元素首尾坐标
        return: [(,),(,)]
        """
        bounds = ele.get_attribute('bounds')
        x_y = re.findall(r'\[(\d+),(\d+)\]', bounds)
        return x_y

    def get_loc_data(self, data_path, loc_str):
        """
        获取定位方法和表达式
        """
        device_yml = {0: "web", 2: "android", 3: "ios"}
        data = YamlUtil(data_path).get_data()[loc_str]
        data = data.get(device_yml[run_device]) if data.get(device_yml[run_device]) else data
        return data

    def element_snapshot(self, case_data_yml, element_loc, method='click', **kwargs):
        """
        元素截图
        """
        data = self.get_loc_data(case_data_yml, element_loc)
        if not data.get('image', None):
            ele_location, ele_size = self.get_element_location(case_data_yml, element_loc)
            save_dir = os.path.dirname(case_data_yml)
            name = element_loc
            # 设备分辨率
            # ------------------iOS------------------
            if run_device == 3:     # iOS端分辨率
                resolution = (2208, 1242)
            # ------------------iOS------------------
            else:
                resolution = self.get_device_resolution()
            name += f"_{str(resolution)}"
            # 获取需要裁剪的最终坐标的起始位置
            size = self.calculate_clip_size(ele_location, ele_size)
            # 截图
            # png_path = self.snapshot() if run_device != 0 else self.get_screen()
            png_path = self.get_screen('jietu.png')
            # 裁剪
            device_name = YamlUtil(os.path.join(CONF_DIR, 'desire_cap.yml')).get_data()['deviceName'] if run_device != 0 else "web"
            # ------------------iOS------------------
            if run_device == 3: # 根据iOS获取对应设备名称
                device_name = YamlUtil(os.path.join(CONF_DIR, 'desire_cap.yml')).get_data()['name'] if run_device != 0 else "web"
            # ------------------iOS------------------
            save_dir = os.path.join(save_dir, device_name, name + '.png')
            self.crop_pic(png_path, save_dir, size)
            return save_dir
        else:
            pass

    def calculate_clip_size(self, ele_location, ele_size):
        """
        计算需要裁剪图片的最终位置坐标
        """
        # 标题栏高度
        title_height = 0
        x = ele_location['x'], ele_location['x'] + ele_size['width']
        y = ele_location['y'] + title_height, ele_location['y'] + title_height + ele_size['height']
        # ------------------iOS------------------
        if run_device == 3: # iOS图像比例因子这里为3
            x = tuple([i*3 for i in x])
            y = tuple([i*3 for i in y])
        # ------------------iOS------------------
        res = x, y
        return res

    def get_device_resolution(self):
        """
        获取设备分辨率
        """
        if run_device == 0:
            resolution = (win32api.GetSystemMetrics(win32con.SM_CXSCREEN), win32api.GetSystemMetrics(win32con.SM_CYSCREEN))
        else:
            resolution = self.driver.get_window_size()
            resolution = (resolution['width'], resolution['height'])
        return resolution

    def crop_pic(self, origin_image_path, target_image_path, size):
        """
        裁剪图片
        """
        img = cv2.imread(origin_image_path)
        cropped = img[size[1][0]:size[1][1], size[0][0]:size[0][1]]
        target_dir = os.path.dirname(target_image_path)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        cv2.imwrite(target_image_path, cropped)
