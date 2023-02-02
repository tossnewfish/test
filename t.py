#search_engine.py
import sys
from collections import deque
import requests
import re
import lxml
from bs4 import BeautifulSoup
import sqlite3
import jieba
i=1

murl=[]
url='http://www.zut.edu.cn/index/xwdt.htm'
unvisited=deque()
visited=set()
unvisited.append(url)
conn=sqlite3.connect('view.db')
c=conn.cursor()
c.execute('drop table doc')
c.execute('create table doc (id int primary key,link text)')
c.execute('drop table word')
c.execute('create table word (term test,list text)')
conn.commit()
conn.close()
print('开始爬取')
cnt=0
while unvisited and cnt<10:
    url=unvisited.popleft()
    visited.add(url)
    cnt +=1
    print ('开始爬取第',cnt,url)

    try:
        r=requests.get(url)
        r=r.text
    except:
        continue
    soup=BeautifulSoup(r,'lxml')
    s_all=soup.find_all('a',{'class':"con fix"})
    for a in s_all:
        x=a.attrs['href']
        if re.match(r'\.\.\/info\/.+',x):
            x='http://www.zut.edu.cn'+x[2:]
        if re.match(r'\/info\/.+',x):
            x='http://www.zut.edu.cn'+x

        if re.match(r'info/.+',x):
            x='http://www.zut.edu.cn/'+x

        if re.match(r'\.\.\/\.\.\/info/.+',x):
            x='http://www.zut.edu.cn'+x[5:]

        if (x not in visited)and(x not in unvisited):
            unvisited.append(x)
    a=soup.find('a',{'class':'Next'})
    if a!=None:
        x=a.attrs['href']
        if re.match(r'xwdt\/.+',x):
            x='https://www.zut.edu.cn/index/'+x
        else:
            x='https://www.zut.edu.cn/index/xwdt/'+x
        if (x not in visited)and(x not in unvisited):
            unvisited.append(x)

    try:
        r = requests.get(url)
        r.encoding='utf_8'
        r=r.text
    except Exception as e:
        print(e)



    soup=BeautifulSoup(r,'html.parser')
    title=soup.title
    if title==None:
        print('此页面不是新闻')
        murl.append(url)
        continue
    else:


        title=soup.title.string

    article=soup.find('p',{'class':'vsbcontent_start'})
    if article==None:
        print('此页面不是新闻')
        murl.append(url)
        continue
    else:

        article=article.get_text()
    author=soup.find('p',{'class':'vsbcontent_end'})
    if author==None:
        print('此页面不是新闻')
        murl.append(url)
        continue
    else:

        author=author.get_text()
    time= soup.find('span',text=re.compile("发布日期"))
    if time==None:
        print('此页面不是新闻')
        murl.append(url)
        continue
    else:

        time=time.get_text()
    seggen=jieba.cut_for_search(title)
    seglist=list(seggen)
    seggen=jieba.cut_for_search(article)
    seglist+=list(seggen)
    seggen=jieba.cut_for_search(time)
    seglist+=list(seggen)
    coon=sqlite3.connect("view.db")
    c=coon.cursor()


    c.execute('insert into doc values (?,?)',(cnt,url))
    for wor in seglist:
        c.execute('select list from word where term = ?',(wor,))
        result=c.fetchall()

        if len(result)==0:


            c.execute('insert into word values (?,?)',(wor,str(cnt)))
        else:
            d=result[0][0]
            d+=' {0}'.format(str(cnt))
            c.execute('update word set list = ? where term = ?',(d,wor))
            if i == 1:
                print(result,d)
                i = 0
    coon.commit()
    coon.close()
    print('词表建立完成')