import pymysql
import os
from win32com import client
import pythoncom
from configparser import ConfigParser

def generalSqlOpeartor(sql_cmd):
    cfg = ConfigParser()
    cfg.read("config.conf")
    db_cfg = dict(cfg.items("database"))
    db_cfg['port'] = int(db_cfg['port'])
    db=pymysql.connect(**db_cfg)
    cursor=db.cursor()
    try:
        cursor.execute(sql_cmd)
        db.commit()
        results = cursor.fetchall()
        return results
    except Exception as err:
        print(err)
        raise err
    finally:
        db.close()
    
def CheckUserLogin(username, password):
    status={
        'status':'False',
        'uid':'',
        'uname':'',
        'uemail':'',
        'enabledUser':-1
    }
    try:
        results = generalSqlOpeartor(f'''select `uid`, `uname`, `uemail`, `enabledUser` from printeruser where uname = '{username}' and upass = substr(MD5("{password}"),9,16);''')
        if len(results)==1:
            status['status']=True
            status['uid']=results[0][0]
            status['uname']=results[0][1]
            status['uemail']=results[0][2]
            status['enabledUser']=results[0][3]
            return status
    except Exception as err:
        print(err)
        raise err
    return status


def CheckUserSignUp(username, password, uemail):

    try:
        results = generalSqlOpeartor(f'''insert into printeruser (`uname`, `upass`, `uemail`, `upaperRemain`) 
values('{username}', substr(MD5("{password}"),9,16),'{uemail}',0);''')
    except Exception as err:
        print(err)
        return False
        raise err    
    else:
        return True


def costBalance(uid, cost, ptime, filename):
    try:
        generalSqlOpeartor("update printerUser set upaperRemain = upaperRemain - {} where `uid`= {} ; ".format(cost,uid))
        generalSqlOpeartor("insert into printerlog (`printtime` ,`uid` ,`printPaper` ,`printFilename`) values('{}',{},{},'{}') ; ".format(ptime,uid,cost,filename))
    except Exception as err:
        print(err)
        raise err

def get_from_id(user_id):
        status={
            'uname':'',
            'uid':user_id,
            'utele':'',
            'upaperRemain':0,
            'enabledUser':-1,
            'isadmin':-1
        }
        if not user_id:
            return None
        try:
            results = generalSqlOpeartor('select uid, uemail, upaperRemain, enabledUser, isadmin from printerUser where uid="{}";'.format(user_id))
            if len(results)==1:
                status['uid']=results[0][0]
                status['uemail']=results[0][1]
                status['upaperRemain']=results[0][2]
                status['enabledUser']=results[0][3]
                status['isadmin']=results[0][4]
                return status
        except Exception as err:
            print(err)
            raise err
        return None

def printfile(filename="",page_0='1',page_1='n',copies=1):
    tmpcfg = ConfigParser()
    tmpcfg.read("config.conf")
    tmpdb_cfg = dict(tmpcfg.items("printer"))
    page_0 = '1' if page_0 =='' else page_0
    page_1 = 'n' if page_1 =='' else page_1
    
    pcommand = 'SumatraPdf.exe -print-to "{}" -print-settings "{}-{},{}x" "{}"'.format(tmpdb_cfg['printername'],page_0, page_1, copies, filename)
    os.system(pcommand)





def doc2pdf(fn):
    # 转换doc为pdf
    pythoncom.CoInitialize()
    fn = fn.replace('/','\\')
    word = client.DispatchEx("Word.Application")  # 打开word应用程序
    # for file in files:
    doc = word.Documents.Open(fn)  # 打开word文件
    doc.SaveAs("{}.pdf".format(fn[:-4]), 17)  # 另存为后缀为".pdf"的文件，其中参数17表示为pdf
    doc.Close()  # 关闭原来word文件
    word.Quit()
    pythoncom.CoUninitialize()   


def docx2pdf(fn):
    # 转换docx为pdf
    pythoncom.CoInitialize()
    fn = fn.replace('/','\\')
    word = client.DispatchEx("Word.Application")  # 打开word应用程序
    # for file in files:
    doc = word.Documents.Open(fn)  # 打开word文件
    doc.SaveAs("{}.pdf".format(fn[:-5]), 17)  # 另存为后缀为".pdf"的文件，其中参数17表示为pdf    
    doc.Close()  # 关闭原来word文件
    word.Quit()
    pythoncom.CoUninitialize()

