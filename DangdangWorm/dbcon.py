# db = pymysql.connect("localhost", "root", "root", "school_db")
# cursor = db.cursor()
# cursor.execute("insert into student1 VALUES('%s','%s','%s')" % (Name, Grade, Class))
# db.commit()
# db.close()
import pymysql
class DbConn(object):
    conn = ""
    cursor = ""
    def __init__(self,ip,name,pwd,dbname):
        self.ip = ip
        self.name = name
        self.pwd = pwd
        self.dbname = dbname
    def DBconnect(self):
        self.conn = pymysql.connect(self.ip,self.name,self.pwd,self.dbname)
        self.cursor = self.conn.cursor()
        return self.cursor
    def Sql(self,sql):
        self.cursor.execute(sql)
    def commit(self):
        self.conn.commit()
    def result(self):
        return self.cursor.fetchall()
    def close(self):
        self.conn.close()