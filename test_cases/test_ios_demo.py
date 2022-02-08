import allure
import pytest
from page_obj.demo.ios_demo_page import IosDemo
import time

class TestIosDemo(object):

    @allure.story('ios端demo用例')
    @pytest.mark.run(order=1)
    def test_ios_demo(self, start_web):
        page = IosDemo(start_web)
        page.check_body()