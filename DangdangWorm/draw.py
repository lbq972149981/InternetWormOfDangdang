import pandas as pd
from pandas import Series, DataFrame
import numpy as np
import pymysql
from text9.dbcon import *
import sys
import pandas
from decimal import *
import matplotlib.pyplot as plt
booktype=[]
booksumcomment=[]
bookavgcomment=[]
bookavgzhekou=[]
booksumcommentpre = []
infor ={}
def getData():
    conn = pymysql.connect("localhost","root","root","school_db")
    cursor = conn.cursor()
    sql = "select * from booktest2"
    cursor.execute(sql)
    books = cursor.fetchall()
    for v in books:
        booktype.append(v[0])
        booksumcomment.append(v[1])
        bookavgcomment.append(v[2].quantize(Decimal('0.00')))
        bookavgzhekou.append(v[3].quantize(Decimal('0.00')))
    conn.commit()
    conn.close()
    for v in booksumcomment:
        pre = v/ sum(booksumcomment)
        booksumcommentpre.append(pre.quantize(Decimal('0.00'))* 100)

def infor():
    infor = {
        "总评论": booksumcomment, "平均评论": bookavgcomment, "总折扣": bookavgzhekou
    }
    data = DataFrame(infor)
    print(data)
def draw():
    labels = booktype
    fracs = booksumcommentpre
    explode = [0, 0, 0, 0,0.1]
    plt.axes(aspect=1)
    plt.pie(x=fracs, labels=labels, explode=explode, autopct='%3.1f %%',
            shadow=True, labeldistance=1.1, startangle=90, pctdistance=0.6)
    plt.show()
if __name__ == '__main__':
    getData()
    infor()
    draw()
