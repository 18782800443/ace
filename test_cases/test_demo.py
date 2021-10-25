import allure
import pytest
from page_obj.container.web_demo_page import DrawerPage
from page_obj.container.app_demo_page import OsAppPage



class TestDemo(object):

    @allure.story('web端demo用例')
    @pytest.mark.run(order=1)
    def test_web_demo(self, start_web):
        page = DrawerPage(start_web)
        page.on_the_d()
        page.on_the_r()
        page.on_the_u()
        page.on_the_l()

    @allure.story('osapp自动截图')
    @pytest.mark.run(order=2)
    def test_app_demo(self, start_web):
        page = OsAppPage(start_web)
        page.open_app()
        page.login()
