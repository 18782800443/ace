from utils.setting import DATA_DIR
import os
from basic_page.base_page import SnapshotPage
# 测试用例配置文件路径
# parent_catalogue = os.getcwd().split(os.sep)[-1]
parent_catalogue = os.path.dirname(os.path.abspath(__file__)).split(os.sep)[-1]
CASE_DATA_YML = os.path.join(DATA_DIR, parent_catalogue, 'app_demo.yml')


class OsAppPage(SnapshotPage):

    def open_app(self):
        pass

    def login(self):
        pass




