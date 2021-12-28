import tkinter as tk
import tkinter.messagebox as msg
import pymysql
import initial
import manager
import reader
import m_operation
import r_operation
def id_check(a): 
    global id
    if a == '1':#在管理员界面下登录，参数是1
    #把账号/密码框框里输入的字符串赋值给id/password
        id = manager.entry_name.get()
        password = manager.entry_key.get()
    else: #在读者界面下登录，参数是0
        id = reader.entry_name.get()
        password = reader.entry_key.get()
    getid()#最后得到id
    #连接数据库，root是你数据库的用户名，应该是默认的是root，qwer是你数据库的密码，library是你要连接的数据库名字
    db = pymysql.connect(host="120.79.31.91", user="visitor", password="1234", database="library")
    #建立游标cursor，这个游标可以类比指针，这样理解比较直观
    cursor = db.cursor()
    sql = "SELECT password, job FROM user WHERE uid='%s'" % (id)
    cursor.execute(sql) #sql语句被执行
    result = cursor.fetchone()#得到的结果返回给result数组
    if result:#如果查询到了账号存在
        if a == result[1]:
            if password == result[0]:#result[0]是数组中的第一个结果
                success_login(a)#密码对上了，进入对应的读者/管理员操作界面
            else:#有账号但密码没对上
               msg._show(title='Error！', message='Account or password typos！')
        else:
            msg.showerror(title='Error！', message='The account has been registered，please enter again！')
    else:#没有账号
        msg._show(title='Error！', message='The user entered does not exist！Please register at first！')
        if a == '1':
            manager.root1.destroy()#关闭登录小窗口，回到管理员界面
        elif a == '0':
            reader.root1.destroy()
    db.close()#查询完一定要关闭数据库啊

def success_login(a):#成功登录
    if a == '1':
        manager.root1.destroy()
        m_operation.frame()#销毁登录注册界面，跳转到管理员的操作界面

    elif a == '0':
        reader.root1.destroy()
        r_operation.frame()#销毁登录注册界面，跳转到读者的操作界面

def success_register(a):#成功登录
    if a == '1':
        manager.root2.destroy()

    elif a == '0':
        reader.root2.destroy()


def id_write(a):#写入（注册）账号
    db = pymysql.connect(host="120.79.31.91", user="visitor", password="1234", database="library")
    cursor = db.cursor()
    if a=='1':#跟check函数里边十分类似
        id = manager.entry_name.get()#得到输入的账号
        password = manager.entry_key.get()#得到输入的密码
        confirm = manager.entry_confirm.get()#得到输入的确认密码
    elif a=='0':
        id = reader.entry_name.get()
        password = reader.entry_key.get()
        confirm = reader.entry_confirm.get()

    sql0 = "SELECT uid FROM user WHERE uid='%s'" % (id)
    sql1 = "INSERT INTO user VALUES('%s','%s','%s') " % (id, password, a)
#首先检查两次输入的密码是否一致，一致后再检查注册的账号是否已经存在
    if password == confirm:
        cursor.execute(sql0)
        result = cursor.fetchone()
        if result:
            msg.showerror(title='Error！', message='The account has been registered，please enter again！')
        else:
            cursor.execute(sql1)
            success_register(a)
            db.commit()
            db.close()
            msg.showinfo(title='Success！', message='Registration successful，please login！')

    else:
        msg.showerror(title='Error！', message='The passwords are inconsistent，please enter again！')

def getid():
    return id