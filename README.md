# Robot-nao

### 说在前面的一些细节
- 主要围绕Nao机器人编程，应用于机器人高尔夫比赛
- Version_1是围绕naoqi API而成的，图像处理和识别都是来自于nao机器人官方自带的API接口实现的。
- Version_2则是对视觉识别部分进行了独立，没有完全沿用API。


### 详细Catalog

- Version_1
  - round1.py~round3.py 是第一杆到第三杆的代码
  - newround.py 是新修改后的代码
  - shijue.py 是老版本中的视觉模块代码
  
- Version_2
  - action.py 运动代码，包括抓杆、挥杆、行走和收杆的动作。
  - ConfigureNao.py 参数配置代码，初始化之类。
  - main-visual-task.py 视觉测试代码。
  - pathplanning.py 路径规划模块代码。
  - task1.py~task3.py 第一杆到第三杆的流程规划代码。
  - visualTask.py 主要的视觉模块代码。

### 高尔夫机器人比赛场景应用描述

- 高尔夫球.docx

### 说在后面
- 资料仅用于学习，如觉得不错star一下！
