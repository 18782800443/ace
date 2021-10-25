#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
from utils.setting import *
from utils.log_util import LogUtil

if __name__ == '__main__':

    logger = LogUtil().get()
    json_report_path = os.path.join(REPORT_DIR, "result")
    html_report_path = os.path.join(REPORT_DIR, "html")
    xml_report_path = os.path.join(REPORT_DIR, "xml")

    args = ['-s', '-q', CASE_DIR, '--alluredir', json_report_path, '--junitxml=%s/report.xml' % xml_report_path]
    pytest.main(args)
    # 生成html测试报告
    cmd = 'allure generate %s -o %s --clean' % (json_report_path, html_report_path)
    try:
        os.system(cmd)
    except Exception as e:
        logger.error("测试报告生成失败")
        raise e

