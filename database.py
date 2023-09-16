import pymysql
from core import generalSqlOpeartor
from configparser import ConfigParser

cfg = ConfigParser()
cfg.read("config.conf")
db_cfg = dict(cfg.items("database"))
db_cfg['port'] = int(db_cfg['port'])
del db_cfg['database']
db=pymysql.connect(**db_cfg)
cursor=db.cursor()
try:
    cursor.execute('''create database IF NOT EXISTS `thinkPrinter`;''')
    db.commit()
    results = cursor.fetchall()
except Exception as err:
    print(err)
    raise err
finally:
    db.close()

sqlcmd =[
f'''create table IF NOT EXISTS printeruser(
`uid` int primary key auto_increment,
`uname`  varchar(20) unique,
`upass`  varchar(50),
`uemail`  varchar(50) unique,
`upaperRemain` int default 0,
`enabledUser` int not null default -1,
`isadmin` int not null default -1);''',
f'''create table IF NOT EXISTS printerlog(
`printtime` datetime  ,
`uid` int ,
`printPaper` int default -1,
`printFilename` varchar(30) );''',
f'''insert into printeruser (`uname`, `upass`, `uemail`, `upaperRemain`, `enabledUser`,`isadmin`) 
values('admin', substr(MD5("zhrnbnbnb666"),9,16),'hangshuicheung@outlook.com',114514,1,1);'''
]
for i in sqlcmd:
    generalSqlOpeartor(i)

