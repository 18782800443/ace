# ace

### 一、项目命名规范

1. 包名、模块名、局部变量名、方法名

```
全小写+下划线拼接 示例：this_is_var
```

- **注**：变量名、类名取名能尽量表示出含义，严禁用单字母
- 变量名不要用系统关键字，如 dir type str等等
- 建议：bool变量一般加上前缀 is_ 如：is_success

2. 类名

```
首字母大写式驼峰 示例：ClassName()
```

3. 全局变量

```
全大写+下划线式驼峰 示例：GLOBAL_VAR
```

### 二、使用说明

1. 项目使用python3，建议3.6+
2. 安装requirements.txt的依赖库
3. 项目根目录建议手动创建report, screenshot,logs三个目录，report目录下创建result和html目录
4. 项目内使用的Android测试demo为哔哩哔哩，可直接运行，正式编写用例后删除相关的demo文件即可
5. 项目内使用的IOS的测试demo为uicatalog，可至https://github.com/appium/ios-uicatalog下载，需要用个人或企业开发者账号重新签名编译
6. 各团队编写用例需单独创建分支，不要合并至master，master作为基础模版供各团队参考

### 三、日志模块

* 模版使用loguru封装了日志的工具类，路径：basic/log_util.py, 可以直接使用也可以用其他的，建议使用loguru，更多使用参考官方文档：https://loguru.readthedocs.io/en/stable/index.html

### 四、基础能力

1. utils目录下setting.py定义了项目的文件目录，以及一些重要参数
    比如：不同的端用run_device参数表示，用dom节点执行还是用图片识别方式执行用例用run_type参数表示，ST.THRESHOLD表示图像识别精准度阈值
2. utils目录下yaml_util.py定义了基础的yaml文件操作，各团队可根据需要使用或修改
3. utils目录下driver.py封装了webdriver，各团队可直接使用或自定义

### 五、数据分离

1. appium地址配置需写在 conf/appium_address.yml文件中，多配置可以写在一个文件内以"---"分割，**注：yaml数据层级不要改变**
2. appium配置信息需写在 conf/desire_cap.yml文件中，Android和IOS配置以"---"分割，顺序不要改变
```
# basic目录下driver中加载ios配置
self.desired_caps = yaml_util.get_all_data()[1]
加载android配置
self.desired_caps = yaml_util.get_all_data()[0]
```
3. 测试用例需在test_cases目录下，要求必须满足pytest的规则约束且测试用例文件必须以"test"开头
4. 测试数据需在test_data目录下，如demo用例，目录层级不要改变
5. 页面类的定义需在page_object目录下，遵循PO理念编写即可，base_page.py已封装一些基础的页面操作方法和自动截图方法

### 六、测试报告

1. 测试报告使用allure第三方测试报告框架，使用方法可参考模版内编写的demo,更多用法参考allure的官方文档：https://docs.qameta.io/allure/
2. 测试报告展示的内容灵活性较强，各团队可根据allure的使用规则自己定义，可能需要单独的封装一些方法或装饰器的添加

### 七、其他说明

1. 模版中目录结构可进行增加，但不要修改，如需修改请联系：牟华
2. conf目录下的已定义的文件名不要修改或删除，可进行增加
3. 模版中定义的方法不做要求，各团队可自定义实现
4. 如有bug或对模版框架有任何意见或建议请联系：牟华