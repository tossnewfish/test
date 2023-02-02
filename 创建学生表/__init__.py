import sqlite3
def opendb():
    coon=sqlite3.connect("studend.db")
    cur=coon.execute("""create table if not exists tongxulu (usernum integer primary key
    ,username varchar(120),password varchar(120),address varchar(125),tel varchar(120))""")
    return cur,coon
def showalldb():
    print("处理后的数据")
    hel=opendb()
    cur=hel[1].cursor()
    cur.execute('select * from tongxulu')
    for line in cur:
        print(line)
    cur.close()
def into():
    usernuml=input("请输入学号")
    usernamel=input("请输入姓名")
    passwordl=input("请输入密码：")
    addressl=input("请输入地址")
    teln=input("请输入电话")
    return usernamel,usernuml,passwordl,addressl,teln
def adddb():
    print("欢迎使用数据库的功能")
    person=into()
    hel=opendb()
    hel[1].executemany('insert into tongxulu values (?,?,?,?,?)',(person,))
    hel[1].commit()
    print("恭喜你数据加载完成")
    showalldb()
    hel[1].close()
def deldb():
    print("欢迎使用数据库的功能")
    dol=input("请输入想要删除的学号")
    hel=opendb()
    hel[1].execute('delete from tongxulu where usernum = ?',(dol,))
    hel[1].commit()
    print("恭喜你数据加载完成")
    hel[1].close()
def alter():
    print("欢迎使用数据库的功能")
    dol = input("请输入想要alter的学号")


    hel = opendb()
    person=into()
    hel[1].execute('update tongxulu set usernum=?,username=?,password=?,address=?,tel=? where usernum=?',(person[0],person[1],person[2],person[3],person[4],dol))
    hel[1].commit()
    showalldb()
    print("恭喜你数据加载完成")
    hel[1].close()
def searchdb():
    print("欢迎使用数据库的功能")
    dol = input("请输入想搜索的学号")
    hel = opendb()
    cur=hel[1].cursor()
    cur.execute('select * from tongxulu where usernum = ?', (dol,))
    hel[1].commit()
    line=cur.fetchall()
    print("恭喜你数据加载完成")

    print(line[0])
    cur.close()
    hel[1].close()
def cont(a):
    choose=input('请选择y or n')
    if choose=='y':
        a=1
    else:
        a=0
    return a
if __name__=="__main__":
    flag=1
    while flag:
        print("欢迎使用通讯录")
        chl='''请选择功能
        【添加】输入数据
        【删除】
        【修改】制定数据
        【查询】
        '''
        ca=input(chl)
        if ca=='添加':
            adddb()
            flag=cont(flag)
        elif ca=='删除':
            deldb()
            flag=cont(flag)
        elif ca=='修改':
            alter()
            flag=cont(flag)
        elif ca=='查询':
            searchdb()
            flag=cont(flag)
        else:
            print("你输入有误")

    else:
        showalldb()



