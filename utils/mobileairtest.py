# -*- coding: utf-8 -*-
import os
from utils.yaml_util import YamlUtil
from utils.setting import CONF_DIR
from airtest.core.api import *

device_cap = YamlUtil(os.path.join(CONF_DIR, 'desire_cap.yml')).get_data()
address_yaml = YamlUtil(os.path.join(CONF_DIR, 'appium_address.yml')).get_data()


def connect_android():
    if "uuid" in device_cap:
        init_device(uuid=device_cap['uuid'])
    else:
        init_device()


def start_android_app():
    if "appPackage" in device_cap:
        app_package = device_cap['appPackage']
        stop_app(app_package)
        start_app(app_package)
    else:
        raise Exception(f"未在{CONF_DIR}/desire_cap.yml找到appPackage")


def input_value(v, value):
    """聚焦到输入框，并键入数据文本"""
    touch(v)
    text(value)


def start_yosemite():
    """启动yosemite"""
    yosemite = G.DEVICE.yosemite_ime
    if not yosemite.started:
        yosemite.start()


@logwrap
def swipe(v1, v2=None, position=None, **kwargs):
    """点击图片拖动到指定位置
        v1: 需要拖动的图片
        v2: 需要拖动到的截图图片位置
        position：(x, y)偏移量
    """
    if isinstance(v1, Template):
        pos1 = loop_find(v1, timeout=ST.FIND_TIMEOUT)
    else:
        try_log_screen()
        pos1 = v1
    if v2:
        if isinstance(v2, Template):
            pos2 = loop_find(v2, timeout=ST.FIND_TIMEOUT_TMP)
        else:
            pos2 = v2
    elif position:
        pos2 = (pos1[0] + position[0], pos1[1] + position[1])
    else:
        raise Exception("no enough params for swipe")

    G.DEVICE.swipe(pos1, pos2, **kwargs)
    delay_after_operation()
    return pos1, pos2


def kill_ios_iproxy():
    output = os.popen('lsof -i tcp:8100 | grep "iproxy"').read()
    if output:
        for line in output.split('\n'):
            if line:
                command, pid = line.split()[:2]
                os.popen(f'kill -9 {pid}')


def connect_ios():
    # kill_ios_iproxy()
    # os.popen('iproxy 8100 8100')
    auto_setup(__file__, devices=["iOS:///http://127.0.0.1:8100"])


def start_ios_app():
    if "bundleId" in device_cap:
        app_package = device_cap['bundleId']
        stop_app(app_package)
        start_app(app_package)
    else:
        raise Exception(f"未在{CONF_DIR}/desire_cap.yml找到bundleId")


if __name__ == '__main__':
    connect_ios()
    start_ios_app()
    time.sleep(3)