import json
import time
import os
from flask import Flask
from flask import render_template
from flask_bootstrap import Bootstrap
from flask import request
from flask import redirect
from flask import url_for
from flask import jsonify
from flask import send_from_directory
from flask_login import LoginManager
from flask_login import current_user, login_required
from flask_login import UserMixin
from flask_login import login_user
from flask_login import logout_user
from flask_admin import Admin
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename

import pymysql
import traceback
from core import *
from PyPDF2 import PdfFileReader
import PyPDF2
from win32com import client
import pythoncom
from datetime import datetime

app = Flask(__name__)


app.secret_key = 'thinkprinter-python_kdjsfhk3y98d' 
app.config['ALLOWED_EXTENSIONS']= set(['pdf','doc', 'docx'])
app.config['MAX_CONTENT_LENGTH']= 1024* 1024 * 1024  # 1GB support
app.config['UPLOAD_PATH'] = '/path/uploads'


login_manager = LoginManager()  # 实例化登录管理对象
login_manager.init_app(app)  # 初始化应用
login_manager.login_view = 'login'  # 设置用户登录视图函数 endpoint

class User(UserMixin):

    def __init__(self, user):
        self.uid=user.get("uid")
        self.uname=user.get("uname")
        self.upass=user.get("upass")
        self.uemail=user.get("uemail")
        self.upaperRemain=user.get("upaperRemain")
        self.enabledUser=user.get("enabledUser")
    
    def checkPassword(uname, upass):
        status = CheckUserLogin(uname, upass)
        self.uid=status.get("uid")
        self.uemail=status.get("uemail")
        self.upaperRemain=status.get("upaperRemain")
        self.enabledUser=status.get("enabledUser")
        return status

    def get_id(self):
        return self.uid

    def get(user_id):
        return User(get_from_id(user_id))
        

@login_manager.user_loader  # 定义获取登录用户的方法
def load_user(user_id):
    return User.get(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'GET':
        return render_template('login.html')

    elif request.method == 'POST':
        print(request.form)
        status={}
        uname = request.values.get('username').strip()
        upass = request.values.get('password').strip()
        if uname =='' or upass=='':
            return redirect('/err?errType=-2')
            return redirect('用户名或密码不可为空')
        try:
            status = CheckUserLogin(uname, upass)
            if status['enabledUser']==-1:
                return redirect('/err?errType=-1')
            else:
                login_user(User(status))
                return redirect('/')
        except Exception as err:
            print(err)
            raise err
        return redirect('/')



     
@app.route('/logout')  # 登出
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    if request.method == 'POST':
        print(request.form)
        username = request.values.get('username').strip()
        password = request.values.get('password').strip()
        uemail=request.values.get('uemail').strip()
        try:
            res=CheckUserSignUp(username, password, uemail)
            if res:
                # return render_template('default.html')
                return redirect('/')
        except Exception as err:
            print(err)
            return redirect('/signup')

@app.route('/err', methods=['GET'])
def errPage():
    err = request.values.get('errType').strip()
    errlist={'-1':'账号密码错误，或账号已被停用',
             '-2':'用户名或密码不可为空'}
    if err in errlist:
        return render_template('err.html', errInfo=errlist.get(err))
    else:
        return render_template('err.html', errInfo="【错误的错误信息！】")

@app.route('/', methods=['GET','POST'])
@login_required
def thinkPrint():
    if request.method=='POST':
        fileList = request.files.getlist('file')
        ptime = int(time.time()*1000)
        copies = request.values.get('copies').strip()
        copies = 1 if copies =='' else int(copies)
        page_0=request.values.get('page_0').strip()
        page_1=request.values.get('page_1').strip()
        appPath="C:/projects/thinkPrinter-python/"   #   os.path.dirname(__file__)
        thisPath=''
        for idx in range(len(fileList)):
            file = fileList[idx]
            
            suffix = os.path.splitext(file.filename)[-1]
            fptime = f'{ptime}_{idx}'
            print(suffix)
            if suffix=='.doc':
                thisPath=appPath+"static/uploads/print_{}.doc".format(fptime)
                file.save(thisPath)
                print(1,thisPath)
                doc2pdf(thisPath)
                thisPath=thisPath[:-3]+'pdf'
            elif suffix=='.pdf':
                thisPath=appPath+"static/uploads/print_{}.pdf".format(fptime)
                print(2,thisPath)
                file.save(thisPath)
            elif suffix=='.docx':
                thisPath=appPath+"static/uploads/print_{}.docx".format(fptime)
                print(3,thisPath)
                file.save(thisPath)
                docx2pdf(thisPath)
                thisPath=thisPath[:-4]+'pdf'
            else:
                return render_template('thinkPrint.html')
                
            pdfFileObj = open(thisPath, 'rb')
            pdfReader = PyPDF2.PdfReader(pdfFileObj)
            num_page = len(pdfReader.pages) * copies 

            costBalance(current_user.uid, num_page,  datetime.fromtimestamp(ptime//1000).strftime('%Y-%m-%d %H:%M:%S'), str(ptime)+suffix)
            printfile(thisPath,page_0=page_0,page_1=page_1,copies=copies)
        return render_template('thinkPrint.html', userInfo=current_user, 
        printAlready=True, num_page=num_page)

    return render_template('thinkPrint.html', userInfo=current_user, printAlready=False)




if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3306, debug=False)
