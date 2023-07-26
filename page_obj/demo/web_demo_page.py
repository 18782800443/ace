from utils.setting import DATA_DIR
import os
from basic_page.base_page import SnapshotPage
import requests
from PIL import Image
import re
import random


class TencentSlider(SnapshotPage):
    def get_track(self, distance):
        track = []
        current = 0
        mid = distance*7/8
        t = random.randint(2,3)/10
        v = 0
        while current < distance:
            if current < mid:
                a = 2
            else:
                a = -3
            v0 = v
            v = v0 + a*t
            move = v0*t + 1/2*a*t*t
            current += move
            track.append(round(move))
        return track

    def calculate_slip_distance(self):
        """计算腾讯滑块的需要拖动的距离"""
        urls = self.get_ele_url()
        imgs = self.download_imgs(urls)
        x = self.get_gap(imgs[0], imgs[1])
        x = x//2 - 38
        [os.remove(f"./image{index}.png") for index in range(len(urls))]
        return x

    def get_ele_url(self):
        """
        获取腾讯滑块验证原图和待缺口图片的图片链接
        """
        self.driver.switch_to.frame("tcaptcha_iframe")
        loc = self.by("xpath", '//img[@id="slideBg"]')
        ele = self.wait_element_visibility(loc)
        # ele = self.wait_element_visibility(self.slider_dic, "slider_pic")
        url1 = ele.get_attribute('src')
        url2 = re.match("^https://[^\*]+", url1).group()
        self.driver.switch_to.default_content()
        return url1, url2

    def download_imgs(self, urls):
        """
        下载图片
        """
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36",
            "Host": "t.captcha.qq.com",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9"
        }
        result = []
        for index, url in enumerate(urls):
            res = requests.get(url, headers=headers, verify=False)
            image_path = f"./image{index}.png"
            with open(image_path, "wb") as f:
                f.write(res.content)
            result.append(Image.open(image_path))
        return result

    def get_gap(self, image1, image2):
        """
        获取缺口偏移量
        :param image1:不带缺口的图片（初始图片）
        :param image2:带缺口的图片（按了滑块的图片）
        :return:缺口偏移量
        """
        left = 60
        for i in range(left, image1.size[0]):
            for j in range(image1.size[1]):
                if not self.is_pixel_equal(image1, image2, i, j):
                    left = i
                    return left
        return left

    def is_pixel_equal(self, image1, image2, x, y):
        """
        判断两个像素是否相同
        :param image1:不带缺口的图片（初始图片）
        :param image2:带缺口的图片（按了滑块的图片
        :param x:位置x
        :param y:位置y
        :return:像素是否相同
        """
        pixel1 = image1.load()[x, y]
        pixel2 = image2.load()[x, y]
        num = 60
        if abs(pixel1[0] - pixel2[0]) < num and abs(pixel1[1] - pixel2[1]) < num and abs(
                pixel1[2] - pixel2[2]) < num:
            return 1
        else:
            return 0


# 测试用例配置文件路径
parent_catalogue = os.path.dirname(os.path.abspath(__file__)).split(os.sep)[-1]
CASE_DATA_YML = os.path.join(DATA_DIR, parent_catalogue, 'web_demo.yml')


class DemoPage(TencentSlider):

    def input_account(self):
        self.sort_operation(CASE_DATA_YML, "input_account", "send_keys", value="escadmin")

    def input_password(self):
        self.sort_operation(CASE_DATA_YML, "input_pwd", "send_keys", value="xxx123")

    def login(self):
        self.sort_operation(CASE_DATA_YML, "login")
        x = self.calculate_slip_distance()
        self.sort_operation(CASE_DATA_YML, "slider", "move_to_gap", position=(x, 0))
