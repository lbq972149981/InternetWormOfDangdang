#coding:utf-8
import pymysql
from text9.dbcon import *
import sys
import pandas
bookzhekou=[]
bookcomment=[]
def getData():
    conn = pymysql.connect("localhost","root","root","school_db")
    cursor = conn.cursor()
    sql = "select * from booktest1"
    cursor.execute(sql)
    books = cursor.fetchall()
    for v in books:
        if v[1]==None:
            continue
        else:
            bookzhekou.append(v[1])
            bookcomment.append(v[2])
    conn.commit()
    conn.close()
if __name__ == '__main__':
    getData()
    print('最高折扣：',max(bookzhekou))
    print('最低折扣:',min(bookzhekou))
    print('平均折扣:',"%.2f"%float(sum(bookzhekou)/len(bookzhekou)))
    x,y = max((bookzhekou.count(x), x) for x in set(bookzhekou))
    print('折扣众数：',y)
    print('最高评论数：',max(bookcomment))
    print('最低评论数：',min(bookcomment))
    print('平均评论数：',"%.2f"%float(sum(bookcomment)/len(bookcomment)))
    x, y = max((bookzhekou.count(x), x) for x in set(bookcomment))
    print('评论数众数：', y)
