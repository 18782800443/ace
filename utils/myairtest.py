import pyautogui
import pyperclip
from pynput.keyboard import Controller, Key
from airtest_selenium.proxy import WebChrome, Button
import time


class MyWebChrome(WebChrome):

    def __init__(self, executable_path="chromedriver", port=0,
                 options=None, service_args=None,
                 desired_capabilities=None, service_log_path=None,
                 chrome_options=None):
        super(MyWebChrome, self).__init__(chrome_options=chrome_options, executable_path=executable_path,
                                        port=port, options=options, service_args=service_args,
                                        service_log_path=service_log_path, desired_capabilities=desired_capabilities)
        self.keyboard = Controller()

    def click_keyboard(self, values):
        """用于模拟键盘键入事件, values表示需要同时按下的内容"""
        for value in values:
            self.keyboard.press(value)
        for value in values:
            self.keyboard.release(value)

    def get_v_location(self, v):
        """获取图片的绝对位置"""
        _pos = self.assert_template(v)
        x, y = _pos
        pos = self._get_left_up_offset()
        return pos[0] + x, pos[1] + y

    def drag_and_move(self, v, position):
        """模拟鼠标拖拽"""
        sleep_time = 0.5
        pos = self.get_v_location(v)
        self.mouse.position = pos
        self.mouse.press(Button.left)
        time.sleep(sleep_time)
        self.mouse.move(5, 5)
        time.sleep(sleep_time)
        self.mouse.move(-5, -5)
        time.sleep(sleep_time)
        self.mouse.move(*position)
        time.sleep(sleep_time)
        self.mouse.release(Button.left)

    def move_mouse(self, v):
        """移动鼠标到指定图片位置"""
        pos = self.get_v_location(v)
        self._move_to_pos(pos)

    def input_value(self, v, value, clear=True):
        """模拟输入数据，当clear为True时，先清空所有内容"""
        self.airtest_touch(v)
        if clear:
            self.click_keyboard([Key.ctrl.value, 'a'])
            self.click_keyboard([Key.delete])
        pyperclip.copy(value)
        pyautogui.hotkey('ctrl', 'v')
