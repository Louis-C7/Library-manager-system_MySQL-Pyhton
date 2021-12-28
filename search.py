import tkinter as tk
import tkinter.messagebox as msg
from tkinter import ttk
import pymysql

def frame():
    global window
    window = tk.Tk()
    window.title('Book Search')
    window.geometry('1200x700')

    tk.Label(window,text='Book Category：',font=('Arial',12)).place(x=180,y=30)

    global lis
    comvalue=tk.StringVar()
    lis=ttk.Combobox(window,textvariable=comvalue,height=10,width=10)
    lis.place(x=300,y=30)
    lis['values']=('All','Humanity','Art','Computer','Technology','Magazine')
    lis.current(0)

    global b_name
    tk.Label(window, text='Book Name：', font=('Arial', 12)).place(x=400, y=30)
    b_name=tk.Entry(window,font=('Arial', 12),width=15)
    b_name.place(x=500,y=30)

    global author
    tk.Label(window, text='Author：', font=('Arial', 12)).place(x=640, y=30)
    author = tk.Entry(window, font=('Arial', 12), width=15)
    author.place(x=700, y=30)

    tk.Button(window,text='Search',font=('Arial', 12), width=10,command=search).place(x=900,y=25)
    global tree#建立树形图
    yscrollbar = ttk.Scrollbar(window, orient='vertical')#右边的滑动按钮
    tree = ttk.Treeview(window, columns=('1', '2', '3', '4', '5'), show="headings",yscrollcommand=yscrollbar.set)
    tree.column('1', width=150, anchor='center')
    tree.column('2', width=150, anchor='center')
    tree.column('3', width=150, anchor='center')
    tree.column('4', width=150, anchor='center')
    tree.column('5', width=150, anchor='center')
    
    tree.heading('1', text='Book Name')
    tree.heading('2', text='Author')
    tree.heading('3', text='Category')
    tree.heading('4', text='Price')
    tree.heading('5', text='Storage')
    tree.place(x=200, y=150)
    yscrollbar.place(x=955,y=150)
    window.mainloop()

def search():
#我用了最原始的方法来动态查询
    global tree#建立树形图
    yscrollbar = ttk.Scrollbar(window, orient='vertical')#右边的滑动按钮
    tree = ttk.Treeview(window, columns=('1', '2', '3', '4', '5'), show="headings",yscrollcommand=yscrollbar.set)
    tree.column('1', width=150, anchor='center')
    tree.column('2', width=150, anchor='center')
    tree.column('3', width=150, anchor='center')
    tree.column('4', width=150, anchor='center')
    tree.column('5', width=150, anchor='center')
    
    tree.heading('1', text='Book Name')
    tree.heading('2', text='Author')
    tree.heading('3', text='Category')
    tree.heading('4', text='Price')
    tree.heading('5', text='Storage')
    tree.place(x=200, y=150)
    yscrollbar.place(x=955,y=150)
    if lis.get()=='All'and b_name.get()=='' and author.get()=='' :
        sql="SELECT DISTINCT(b1.name), b1.author, b1.type, b1.price, tb2.storage FROM \
            (SELECT tb1.name, tb1.type, COUNT(*) as storage \
                FROM (SELECT b.bid, b.name, b.type FROM book b WHERE b.bid NOT IN (SELECT bid FROM borrow)) tb1 \
                    GROUP BY tb1.name, tb1.type) tb2, book b1 WHERE b1.name=tb2.name AND b1.type=tb2.type"
    elif lis.get()=='All'and b_name.get()=='' and author.get()!='' :
        sql="SELECT DISTINCT(b1.name), b1.author, b1.type, b1.price, tb2.storage FROM \
            (SELECT tb1.name, tb1.type, COUNT(*) as storage \
                FROM (SELECT b.bid, b.name, b.type FROM book b WHERE b.bid NOT IN (SELECT bid FROM borrow)) tb1 \
                    GROUP BY tb1.name, tb1.type) tb2, book b1 WHERE b1.name=tb2.name AND b1.type=tb2.type AND b1.author='%s'"%(author.get())
    elif lis.get()=='All'and b_name.get()!='' and author.get()=='' :
        sql = "SELECT DISTINCT(b1.name), b1.author, b1.type, b1.price, tb2.storage FROM \
            (SELECT tb1.name, tb1.type, COUNT(*) as storage \
                FROM (SELECT b.bid, b.name, b.type FROM book b WHERE b.bid NOT IN (SELECT bid FROM borrow)) tb1 \
                    GROUP BY tb1.name, tb1.type) tb2, book b1 WHERE b1.name=tb2.name AND b1.type=tb2.type AND b1.name='%s'" % (b_name.get())
    elif lis.get() != 'All'  and b_name.get() =='' and author.get() == '' :
        sql = "SELECT DISTINCT(b1.name), b1.author, b1.type, b1.price, tb2.storage FROM \
            (SELECT tb1.name, tb1.type, COUNT(*) as storage \
                FROM (SELECT b.bid, b.name, b.type FROM book b WHERE b.bid NOT IN (SELECT bid FROM borrow)) tb1 \
                    GROUP BY tb1.name, tb1.type) tb2, book b1 WHERE b1.name=tb2.name AND b1.type=tb2.type AND b1.type='%s'" % (lis.get())
    elif lis.get()=='All'and b_name.get() !='' and author.get()!= '' :
        sql = "SELECT DISTINCT(b1.name), b1.author, b1.type, b1.price, tb2.storage FROM \
            (SELECT tb1.name, tb1.type, COUNT(*) as storage \
                FROM (SELECT b.bid, b.name, b.type FROM book b WHERE b.bid NOT IN (SELECT bid FROM borrow)) tb1 \
                    GROUP BY tb1.name, tb1.type) tb2, book b1 WHERE b1.name=tb2.name AND b1.type=tb2.type \
                        AND b1.name='%s' AND b1.author='%s'" % (b_name.get(),author.get())
    elif lis.get() != 'All' and b_name.get() !='' and author.get() == '' :
        sql = "SELECT DISTINCT(b1.name), b1.author, b1.type, b1.price, tb2.storage FROM \
            (SELECT tb1.name, tb1.type, COUNT(*) as storage \
                FROM (SELECT b.bid, b.name, b.type FROM book b WHERE b.bid NOT IN (SELECT bid FROM borrow)) tb1 \
                    GROUP BY tb1.name, tb1.type) tb2, book b1 WHERE b1.name=tb2.name AND b1.type=tb2.type \
                         AND b1.type='%s' AND b1.name='%s'" % (lis.get(),b_name.get())
    elif lis.get() != 'All' and b_name.get() =='' and author.get() != '' :
        sql = "SELECT DISTINCT(b1.name), b1.author, b1.type, b1.price, tb2.storage FROM \
            (SELECT tb1.name, tb1.type, COUNT(*) as storage \
                FROM (SELECT b.bid, b.name, b.type FROM book b WHERE b.bid NOT IN (SELECT bid FROM borrow)) tb1 \
                    GROUP BY tb1.name, tb1.type) tb2, book b1 WHERE b1.name=tb2.name AND b1.type=tb2.type \
                         AND b1.type='%s' AND b1.author='%s'" % (lis.get(), author.get())
    else :
        sql = "SELECT DISTINCT(b1.name), b1.author, b1.type, b1.price, tb2.storage FROM \
            (SELECT tb1.name, tb1.type, COUNT(*) as storage \
                FROM (SELECT b.bid, b.name, b.type FROM book b WHERE b.bid NOT IN (SELECT bid FROM borrow)) tb1 \
                    GROUP BY tb1.name, tb1.type) tb2, book b1 WHERE b1.name=tb2.name AND b1.type=tb2.type \
                         AND b1.type='%s' AND b1.name='%s' AND b1.author='%s'" % (lis.get(),b_name.get(), author.get())

    db = pymysql.connect(host="120.79.31.91", user="visitor", password="1234", database="library")
    cursor = db.cursor()
    cursor.execute(sql)
    results=cursor.fetchall()
    if results:
        l= len(results)
        for i in range(0,l):#查询到的结果依次插入到表格中
            tree.insert('',i,values=(results[i]))
    else :
        tree.insert('', 0,values=('No Search Result','No Search Result','No Search Result','No Search Result','No Search Result'))

    db.close()