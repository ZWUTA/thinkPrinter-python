import pymysql


def sqlOperator(sqlCommand):
    try:
        db=pymysql.connect(host='localhost', user='root', password='Sby5201314', port=666, database='studentdb')
        cursor=db.cursor()
        cursor.execute(sqlCommand)
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
        'sname':'',
        'uid':'',
        'sid':''
    }
    try:
        db=pymysql.connect(host='localhost', user='root', password='Sby5201314', port=666, database='thinkPrinter')
        cursor=db.cursor()
        cursor.execute('select UId, Sid, Sname from users where username="{}" and password="{}";'.format(username,password))
        db.commit()

        results = cursor.fetchall()
        if len(results)==1:
            status['status']=True
            status['uid']=results[0][0]
            status['sid']=results[0][1]
            status['sname']=results[0][2]
            return status
    except Exception as err:
        print(err)
        raise err
    finally:
        db.close()
    return status


def CheckUserSignUp(username, password, utele):

    try:
        db=pymysql.connect(host='localhost', user='root', password='Sby5201314', port=666, database='thinkPrinter')
        cursor=db.cursor()
        cursor.execute("insert into printerUser (`uname`,`upass`,`utele`) values ('{}', '{}', '{}');".format(username,password,utele))
        db.commit()
    except Exception as err:
        print(err)
        return False
        raise err
        
    else:
        return True
        
    finally:
        db.close()


def costBalance(uid, cost, ptime, filename):
    try:
        db=pymysql.connect(host='localhost', user='root', password='Sby5201314', port=666, database='thinkPrinter')
        cursor=db.cursor()
        cursor.execute("update printerUser set upaperRemain = upaperRemain - {} where `uid`= {} ; ".format(cost,uid))
        db.commit()
        cursor.execute("insert into printlog (`printtime` ,`uid` ,`printPaper` ,`printFilename`) values('{}',{},{},'{}') ; ".format(ptime,uid,cost,filename))
        db.commit()

        return 1

    except Exception as err:
        print(err)
        raise err
    finally:
        db.close()


def getStudentCourse(sno):
    try:
        db=pymysql.connect(host='localhost', user='root', password='Sby5201314', port=666, database='studentdb')
        cursor=db.cursor()
        cursor.execute("select cid,cno, cname, cpno, ccredit from course where cno in (select sc.cno from course, sc, student where course.cno=sc.cno and sc.sno=student.sno and sc.sno='{}');".format(sno))
        db.commit()
        results1 = cursor.fetchall()

        cursor.execute("select cid,cno, cname, cpno, ccredit from course where cno not in (select sc.cno from course, sc, student where course.cno=sc.cno and sc.sno=student.sno and sc.sno='{}');".format(sno))
        db.commit()
        results2 = cursor.fetchall()
        return results1, results2

    except Exception as err:
        print(err)
        raise err
    finally:
        db.close()


def addStuCourse(sno, cno):
    try:
        db=pymysql.connect(host='localhost', user='root', password='Sby5201314', port=666, database='studentdb')
        cursor=db.cursor()
        cursor.execute("insert into sc (`cno`,`sno`) values ('{}','{}')".format(cno, sno))
        db.commit()

        results = cursor.fetchall()
        return results
    except Exception as err:
        print(err)
        raise err
    finally:
        db.close()

def minusStuCourse(sno, cno):
    try:
        db=pymysql.connect(host='localhost', user='root', password='Sby5201314', port=666, database='studentdb')
        cursor=db.cursor()
        cursor.execute("delete from sc where `cno`='{}' and `sno`='{}' ;".format(cno, sno))
        db.commit()

        results = cursor.fetchall()
        return results
    except Exception as err:
        print(err)
        raise err
    finally:
        db.close()


def getGradeInfo():
    try:
        db=pymysql.connect(host='localhost', user='root', password='Sby5201314', port=666, database='studentdb')
        cursor=db.cursor()
        cursor.execute('''select sc.sno,student.sname, sc.cno, course.cname, sc.grade from student, sc, course
         where student.sno=sc.sno and sc.cno=course.cno; ''')
        db.commit()

        results = cursor.fetchall()
        return results
    except Exception as err:
        print(err)
        raise err
    finally:
        db.close()

def getGradeInfo2(a,b,c,d):
    try:
        db=pymysql.connect(host='localhost', user='root', password='Sby5201314', port=666, database='studentdb')
        cursor=db.cursor()
        cursor.execute('''select sc.sno,student.sname, sc.cno, course.cname, sc.grade from student, sc, course
         where student.sno=sc.sno and sc.cno=course.cno and {}.{} {} '{}'; '''.format(a,b,c,d))
        db.commit()

        results = cursor.fetchall()
        return results
    except Exception as err:
        print(err)
        raise err
    finally:
        db.close()


def updateGrade(sno, cno, grade):
    try:
        db=pymysql.connect(host='localhost', user='root', password='Sby5201314', port=666, database='studentdb')
        cursor=db.cursor()
        cursor.execute('''update sc set grade={}  where sno='{}' and cno='{}' ;'''.format(grade, sno, cno))
        db.commit()

        results = cursor.fetchall()
        return results
    except Exception as err:
        print(err)
        raise err
    finally:
        db.close()