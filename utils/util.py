#! encoding:utf-8
import os


def get_pic_name(path, name):
    """根据name模糊查询path路径下的文件"""
    res = []
    for file in os.listdir(path):
        if file.startswith(name) and file.endswith(".png"):
            res.append(file)
    if not res:
        raise Exception(f'未找到包含名称：{name}的图片')
    elif len(res) != 1:
        raise Exception(f'根据{name}在路径{path}下找到多个匹配图片:{str(res)}')
    res_path = os.path.join(path, res[0])
    return res_path
