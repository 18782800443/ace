# -*- coding: utf-8 -*-

"""
封装log方法
"""

from loguru import logger
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class LogUtil:

    def __init__(self):
        """
        rotation:当前配置为按天输出日志文件，也可设置按文件大小，如 rotation="500 MB"
        retention：当前设置日志文件最长保留 7天
        """
        # 错误日志
        logger.add(
            os.path.join(BASE_DIR, "logs/{time:YYYY-MM-DD}/error.log"),
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
            filter=lambda x: True if x["level"].name == "ERROR" else False,
            rotation="00:00", retention=7, level='ERROR', encoding='utf-8'
        )
        # 成功日志
        logger.add(
            os.path.join(BASE_DIR, "logs/{time:YYYY-MM-DD}/success.log"),
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
            filter=lambda x: True if x["level"].name == "SUCCESS" else False,
            rotation="00:00", retention=7, level='SUCCESS', encoding='utf-8'
        )
        # Default日志,会输出所有level日志
        logger.add(
            os.path.join(BASE_DIR, "logs/{time:YYYY-MM-DD}/log.log"),
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
            rotation="00:00", retention=7, level='DEBUG', encoding='utf-8'
        )

        self.logger = logger

    def get(self):
        return self.logger

