# thinkPrinter-python
思考·智慧打印，thinkprinter-go的python版本。jwb现行打印系统

## 系统设计和打印逻辑

MySQL数据库的基本的用户登录与权限管理功能+SumatraPdf的命令行打印功能。

## 支持的功能

 - 多文件批量列印
 - 
## 计划支持的功能
 - SQLite和MySQL双栈数据库
 - 多打印机管理
 - 管理后台


# 部署教程

因使用了win32 api进行pdf转换（基于word），需要在Windows上运行。（本项目使用Canon LBP2900打印机进行测试，该打印机仅在Windows上可调试正常打印 => 对于其他打印机可自行移植至Linux，并替换SumatraPdf为其他打印后端）部署thinkPrinter只需要安装好MySQL数据库，python安装如下库。

```pip install -r requirements.txt```

这里端口号记得改成合适的。
```app.run(host="0.0.0.0", port=3306, debug=False)```
