# search.engine_use.py
import re
import requests
import lxml
from collections import deque
from bs4 import BeautifulSoup
import sqlite3
import jieba
import math
biaoji=0
coon=sqlite3.connect('view.db')
c=coon.cursor()
c.execute('select count(*) from doc')
e=c.fetchall()
n=1+e[0][0]              #文档总数
print(e)
print(n)
target=input("请输入关键词")
seggen=jieba.cut_for_search(target)
score={}                #文档名：得分
for wor in seggen:
    print('得到查询词',wor)
    tf={}               #文档号：出现次数
    c.execute('select list from word where term = ?',(wor,))
    result=c.fetchall()
    if len(result)>0:
        dl=result[0][0]
        dl=dl.split()
        dl=[int(x) for x in dl]
        df=len(set(dl))
        idf=math.log(n/df)          #计算idf
        for num in dl:
            if num in tf:
                tf[num]+=1
            else:
                tf[num]=1
        #tf计算计算开始计算score
        for num in tf:
            if num in score:
                score[num]+=tf[num]+idf
            else:
                score[num]=tf[num]+idf
scoredist=sorted(score.items(),key=lambda d:d[1],reverse=True)  #对score按字典的值排序
cnt=0
for num,doc in scoredist:
    cnt+=1
    c.execute('select link from doc where id = ?',(num,))
    url=c.fetchall()[0][0]
    print(url,'得分',doc)
    try:
        r=requests.get(url)
        r.encoding = 'utf_8'
        r=r.text
    except:
        print('网页出错')
        continue
    soup=BeautifulSoup(r,'lxml')
    title=soup.title
    if title==None:
        print('no')
    else:
        title=title.string
        print(title)
    if cnt>10:
        break
if cnt==0:
    print('无搜索结果')


