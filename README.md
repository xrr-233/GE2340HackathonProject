# GE2340HackathonProject
因为已经私有了 那我就用中文打 大家都看得懂

## 试一试黑客松

### 链接

为了方便访问 在此把所有相关链接放置于此

* 共享Report模板

https://docs.google.com/document/d/1TG3_h5EHDksCA8Txf1GN5Vv41esOtmRsXArG0DyZbE8/edit

* 试题

https://2021.spaceappschallenge.org/challenges/statements/mapping-space-trash-in-real-time/details

* WorldWind javascript版 入门

https://worldwind.arc.nasa.gov/web/get-started/#anchor

* 其他待分析资源

https://data.nasa.gov/browse?q=space%20debris&sortBy=relevance

https://orbitaldebris.jsc.nasa.gov/quarterly-news/

https://donnees-data.asc-csa.gc.ca/en/dataset/9ae3e718-8b6d-40b7-8aa4-858f00e84b30

### 文件结构讲解

该项目采用Flask框架制作

apps文件夹：是python代码区，可以理解为后端的计算，其中又有文件夹，代表不同页面的后端操作；而__init__则作为初始化apps之用

static文件夹：存放各种文件，比如image、css、javascript

template文件夹：称作模板，专门用于渲染html

app.py：主程序，点击播放即可直接生成一个网站，点进去就可以看到结果

建议使用**Pycharm IDE专业版**（学生免费）并载入Flask框架运行此项目

### 目前工作

已经用npm在static中下载了一个WorldWind javascript包并做了些startup
