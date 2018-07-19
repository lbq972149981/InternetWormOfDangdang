#dangdang
#coding:utf8
from bs4 import BeautifulSoup
import re
import urllib
from urllib.request import urlopen
from urllib.error import HTTPError
from distutils.filelist import findall
import pymysql
from text9.dbcon import *
import sys
import re
import decimal
import time
import threading
import queue
j = 0
class dangdang():
    def __init__(self,url,j,bookname,bookinfor,bookprice_now,bookprice_pre,bookcomment,bookauthor,bookpublishtime,bookpublish,menu):
        self.url = url
        self.j = j
        self.bookname=bookname
        self.bookinfor=bookinfor
        self.bookprice_now=bookprice_now
        self.bookprice_pre=bookprice_pre
        self.bookcomment=bookcomment
        self.bookauthor=bookauthor
        self.bookpublishtime=bookpublishtime
        self.bookpublish=bookpublish
        self.menu = menu
    def getHtml(self):
        html = urlopen(self.url).read()
        html = html.decode("gbk")
        soup = BeautifulSoup(html,'html.parser')
        return soup
    def setLi(self,li):
        self.li = li
    def myformat(self,s):
        return s[1:]
    def getBookName(self):
        la = self.li.find("a", class_="pic")
        # 获取li.a.title值 即为bookname
        la_title = la.get("title")
        self.bookname.append(la_title)
    def getBookInfor(self):
        lp_name = self.li.find("p", class_="name")
        # 获取li.p.a的值即为bookinfor
        pa = lp_name.find("a")
        pav = pa.get_text()
        self.bookinfor.append(pav)
    def numformat(self,f, n):
        if round(f) == f:
            m = len(str(f)) - 1 - n
            if f / (10 ** m) == 0.0:
                return f
            else:
                return float(int(f) / (10 ** m) * (10 ** m))
        return round(f, n - len(str(int(f)))) if len(str(f)) > n + 1 else f
    def getPrice(self):
        # 获取当前价格
        lp_price = self.li.find("p", class_="price")
        lpspan_nowprice = lp_price.find("span", class_="search_now_price")
        if  lpspan_nowprice!= None:
            lpspan_nowprice = lpspan_nowprice.get_text()
            nowprice = float(self.myformat(lpspan_nowprice))
        else:
            nowprice = 0
        self.bookprice_now.append(nowprice)
        # 获取之前价格
        lpspan_preeprice = lp_price.find("span", class_="search_pre_price")
        if  lpspan_preeprice != None:
            lpspan_preprice = lpspan_preeprice.get_text()
            preprice = float(self.myformat(lpspan_preprice))
        else:
            preprice = 0
        self.bookprice_pre.append(preprice)
        # # 获取折扣
        # lpspan_discount = lp_price.find("span", class_="search_discount").get_text()
        # bookdiscount.append(lpspan_discount)
    def getComment(self):
        # 获取li.p标签 class为search_star_line 获取评论
        lp_search_star_line = self.li.find("p", class_="search_star_line")
        lpa_comment = lp_search_star_line.find("a", class_="search_comment_num").get_text()
        self.bookcomment.append(int(lpa_comment[:len(lpa_comment)-3]))
    def getAuthor(self):
        # 获取li.p标签 class为search_book_author
        lp_search_book_author = self.li.find("p", class_="search_book_author")
        self.spans = lp_search_book_author.findAll("span")
        # 获取作者
        if self.spans[0].find("a") != None:
            m = 0
            newauthor = ""
            author = self.spans[0].find("a").get("title")
            for i in range(len(author)):
                if author[i] == "[" or author[i] == "（" or author[i]=="(":
                    m = i
                    author = author[m + 3:]
                    author =author.strip()
                    break
            self.bookauthor.append(author)
        else:
            self.bookauthor.append("null")
    def getPublishTime(self):
        # 获取出版日期
        self.bookpublishtime.append(self.spans[1].get_text()[2:])
    def getPublisher(self):
        # 获取出版社
        self.bookpublish.append(self.spans[2].find("a").get("title"))
    def Get(self):
        self.getBookName()
        self.getBookInfor()
        self.getPrice()
        self.getComment()
        self.getAuthor()
        self.getPublishTime()
        # self.getPublisher()
    def ConnDB(self,book_id,book_name,book_infor,bookprice_now,bookprice_pre,book_comment,book_author,book_publishdate):
        conn = DbConn("localhost","root","root","school_db")
        cursor = conn.DBconnect()
        sql = "insert into dangdang_t VALUES('%s','%s','%s','%s','%s','%s','%s','%s')" % (book_id,book_name,book_infor,bookprice_now,bookprice_pre,book_comment,book_author,book_publishdate)
        conn.Sql(sql)
        conn.commit()
        conn.close()
#menu = [bookname, bookinfor, bookprice_now, bookprice_pre, bookcomment, bookauthor, bookpublishtime, bookpublish]
    def insertData(self):
        for i in range(60):
            self.ConnDB(self.j,self.bookname[i],self.bookinfor[i],self.bookprice_now[i],self.bookprice_pre[i],self.bookcomment[i],self.bookauthor[i],self.bookpublishtime[i])
            self.j = self.j+1
        return self.j
    def Print(self):
        for val in self.menu:
            print(len(val),val)
#多线程爬取多个url内容
class mythreading():
    def __init__(self,myqueue):
        self.bookname = []
        self.bookinfor = []
        self.bookprice_now = []
        self.bookprice_pre = []
        self.bookcomment = []
        self.bookauthor = []
        self.bookpublishtime = []
        self.bookpublish = []
        self.menu = [self.bookname, self.bookinfor, self.bookprice_now, self.bookprice_pre, self.bookcomment, self.bookauthor, self.bookpublishtime]
    def func(self,i):
        if not myqueue.empty():
            book = dangdang(myqueue.get(),j,self.bookname,self.bookinfor,self.bookprice_now,self.bookprice_pre,self.bookcomment,self.bookauthor,self.bookpublishtime,self.bookpublish,self.menu)
            soup = book.getHtml()
            ul = soup.find_all("ul", "bigimg")[0]
            for i in range(1, 61):
                li = ul.find("li", class_="line" + str(i))
                book.setLi(li)
                book.Get()
            book.Print()
    def run(self):
        for k in range(5):
            threading.Thread(target=self.func(i),args=(k,)).start()
if __name__ == '__main__':
    while 1:
        print("欢迎来到当当网")
        print("请输入你想要查询的书籍的名称：")
        value = input()
        #队列用于存储多个url
        global myqueue
        myqueue= queue.Queue(maxsize=10)
        for i in range(1,6):
            url = 'http://search.dangdang.com/?key=' + value + '&act=input&page_index=' + str(i)
            myqueue.put(url)
        th=mythreading(myqueue)
        th.run()