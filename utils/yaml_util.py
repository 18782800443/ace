import yaml
from utils.log_util import LogUtil


class YamlUtil:

    def __init__(self, file_path):
        self.file_path = file_path

    # 读取yaml文件数据
    def get_data(self):
        try:
            with open(self.file_path, "r", encoding="utf8") as f:
                context = yaml.load(f, Loader=yaml.FullLoader)
            return context
        except Exception as e:
            LogUtil().get().error("yaml文件不存在" + self.file_path)
            raise e

    # 读取yaml文件中包含多组数据
    def get_all_data(self):
        try:
            with open(self.file_path, "r", encoding="utf8") as f:
                context = yaml.load_all(f, Loader=yaml.FullLoader)
                yaml_data_list = []
                for yaml_data in context:
                    yaml_data_list.append(yaml_data)
                return yaml_data_list
        except Exception as e:
            LogUtil().get().error("yaml文件不存在" + self.file_path)
            raise e

    # 数据写入到yaml文件
    def write_yaml(self, yaml_data):
        try:
            with open(self.file_path, "w", encoding="utf8") as f:
                yaml.dump(data=yaml_data, stream=f, allow_unicode=True)
        except Exception as e:
            LogUtil().get().error("写入yaml文件内容失败")
            raise e
        else:
            LogUtil().get().success("写入yaml文件内容成功")

    # 多组数据写入到yaml文件,documents格式为list
    def write_all_yaml(self, documents):
        try:
            with open(self.file_path, "w", encoding="utf8") as f:
                yaml.dump_all(documents=documents, stream=f, allow_unicode=True)
        except Exception as e:
            LogUtil().get().error("写入yaml文件内容失败")
            raise e
        else:
            LogUtil().get().success("写入yaml文件内容成功")

