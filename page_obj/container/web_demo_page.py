from utils.setting import DATA_DIR
import os
from basic_page.base_page import SnapshotPage
# 测试用例配置文件路径
parent_catalogue = os.path.dirname(os.path.abspath(__file__)).split(os.sep)[-1]
CASE_DATA_YML = os.path.join(DATA_DIR, parent_catalogue, 'web_demo.yml')



class DrawerPage(SnapshotPage):

    def on_the_d(self):
        pass

    def on_the_r(self):
        pass

    def on_the_u(self):
        pass

    def on_the_l(self):
        pass



