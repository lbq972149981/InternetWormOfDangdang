#coding:gbk
import pymysql
import csv
import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import matplotlib.pyplot as plt
import matplotlib
bookauthor = []
bookpubsum = []
bookauthor=["a","b","c","d","e","f"]
book = csv.reader(open('author与sum.csv', encoding='utf-8'))
j = 1
strs = ""
for row in book:
    if j == 1:
        j = j -1
        continue
    strs =strs + str(row[0])+'  '
    bookpubsum.append(int(row[1]))
print(bookauthor)
print(bookpubsum)
print(strs)
myfont = matplotlib.font_manager.FontProperties(fname='C:\Windows\Fonts\simkai.ttf')
matplotlib.rcParams['axes.unicode_minus']=False
X = bookauthor
Y = bookpubsum
plt.bar(X,Y)
plt.xlabel(strs,fontproperties=myfont)
plt.ylabel("书籍出版数",fontproperties=myfont)
plt.title("作者与出版书数量的关系图",fontproperties=myfont)
plt.legend(prop=myfont)
plt.show()
