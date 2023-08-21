from core import generalSqlOpeartor
from configparser import ConfigParser

cfg = ConfigParser()
cfg.read("config.conf")
db_cfg = dict(cfg.items("database"))

sqlcmd =[
f'''create database IF NOT EXISTS {db_cfg["database"]};''',
f'''create table IF NOT EXISTS printeruser(
`uid` int primary key auto_increment,
`uname`  varchar(20) unique,
`upass`  varchar(20)  ,
`utele`  varchar(20) unique,
`upaperRemain` int default 0,
`enabledUser` not null YES default -1,
`isadmin` not null default -1 );''',
f'''create table IF NOT EXISTS printeruser(
`printtime` datetime  ,
`uid`  int ,
`printPaper` int default -1,
`printFilename` varchar(30) );''',
f'''insert into printeruser (`uname`, `upass`, `utele`, `upaperRemain`, `enabledUser`,`isadmin`) 
values('admin', 'admin','12378909876',1);'''
]
for i in sqlcmd:
    generalSqlOpeartor(i)

