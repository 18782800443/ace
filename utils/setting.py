import os
from airtest.core.api import *
from airtest.utils.logger import get_logger
import logging

# 获取项目所在的绝对路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 测试数据所在的目录路径
DATA_DIR = os.path.join(BASE_DIR, "test_data")
DATA_DIR_PAD = os.path.join(BASE_DIR, "test_data", 'pad')

# 测试用例所在的目录路径
CASE_DIR = os.path.join(BASE_DIR, "test_cases")

# 配置文件所在的目录路径
CONF_DIR = os.path.join(BASE_DIR, "conf")

# 测试报告所在的目录路径
REPORT_DIR = os.path.join(BASE_DIR, "report")

# 日志文件所在的目录路径
LOG_DIR = os.path.join(BASE_DIR, "logs")
ST.LOG_DIR = os.path.join(BASE_DIR, "logs")

# 错误截图的路径
ERROR_IMG = os.path.join(BASE_DIR, "screenshot")

# 工具包路径
UTILS_DIR = os.path.join(BASE_DIR, "utils")

# picture路径
PIC_PATH = os.path.join(BASE_DIR, "picture")

# 图像识别准确率默认阈值
ST.THRESHOLD = 0.95
ST.DEBUG = True

# 图像识别超时时间
ST.FIND_TIMEOUT = 10

# 浏览器默认打开时的大小,默认为当前分辨率大小
# DRIVER_SIZE = (win32api.GetSystemMetrics(win32con.SM_CXSCREEN), win32api.GetSystemMetrics(win32con.SM_CYSCREEN))
DRIVER_SIZE = (945, 1020)

# chromedriver路径
DRIVER_PATH = "C:\\chrome\\chromedriver.exe"

# airtest日志，以及重新设置日志级别
logger = get_logger('airtest')
logger.setLevel(logging.DEBUG)

# 0表示web， 1表示pad, 2表示android_phone, 3表示ios_phone
run_device = 3

# 0表示原生xpath元素定位，1表示通过xpath元素截图(生成需要通过图片跑用例的形式)，2表示通过完全通过图片跑脚本
run_type = 1
