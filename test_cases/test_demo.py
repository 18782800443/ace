import allure
import pytest
from page_obj.demo.web_demo_page import DemoPage
import time

class TestDemo(object):

    @allure.story('web端demo用例')
    @pytest.mark.run(order=1)
    def test_web_demo(self, start_web):
        page = DemoPage(start_web)
        page.driver.get("https://testpartner.dmall.com")
        time.sleep(5)
        page.input_account()
        page.input_password()
        page.login()

    # @allure.story('osapp自动截图')
    # @pytest.mark.run(order=2)
    # def test_app_demo(self, start_web):
    #     page = OsAppPage(start_web)
    #     page.open_app()
    #     page.login()
