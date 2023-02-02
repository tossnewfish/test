import re
import requests
from bs4 import BeautifulSoup
import jieba
import sqlite3
url='https://www.zut.edu.cn/info/1041/25820.htm'
cnt=1
try:
    r = requests.get(url)
    r.encoding='utf_8'
    r=r.text
except Exception as e:
    print(e)



soup=BeautifulSoup(r,'html.parser')
title=soup.title.string
article=soup.find('p',{'class':'vsbcontent_start'})
article=article.get_text()
author=soup.find('p',{'class':'vsbcontent_end'})
author=author.get_text()
time= soup.find('span',text=re.compile("发布日期"))
time=time.get_text()
seggen=jieba.cut_for_search(title)
seglist=list(seggen)
seggen=jieba.cut_for_search(article)
seglist+=list(seggen)
seggen=jieba.cut_for_search(time)
seglist+=list(seggen)
coon=sqlite3.connect("view.db")
c=coon.cursor()
c.execute('drop table doc')
c.execute('create table doc (id int primary key,link text)')
c.execute('drop table word')
c.execute('create table word (term test,list text)')
c.execute('insert into doc values (?,?)',(cnt,url))
for wor in seglist:


    c.execute('insert into word values (?,?)',(wor,str(cnt)))
coon.commit()
coon.close()
print('词表建立完成')





