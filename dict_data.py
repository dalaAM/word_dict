"""
database:

"""

import pymysql

class MyDatabase:
    #连接数据库
    def __init__(self):
        self.db =pymysql.connect(host = 'localhost',
                                 port = 3306,
                                 user = 'root',
                                 password ='123456',
                                 database = 'dict',
                                 charset ='utf8')
    #建立游标对象
    def cursor(self):
        self.cursor =self.db.cursor()

    #关闭数据库
    def close(self):
        self.cursor.close()
        self.db.close()

#处理数据
class DataHaddle(MyDatabase):
    #注册
    def do_register(self,name,passwd):
        #查询数据
        sql ="select username from stu where username = %s;"
        self.cursor.execute(sql,[name])
        result = self.cursor.fetchone() #获取一个结果
        if result: #如果查询到结果
            return True
        #插入数据
        sql = "insert into stu (username,password)values(%s,%s);"
        try:
            self.cursor.execute(sql, [name,passwd])
            self.db.commit() #将数据提交给数据库
        except Exception:
            self.db.rollback() #提交失败则回滚

    #登录
    def do_login(self,name,passwd):
        #查询数据
        try:
            sql ="select username,password from stu where username = %s and  password =%s;"
            self.cursor.execute(sql,[name,passwd])
        except Exception as e:
            if e: #如果有异常
                return False #返回flase
        else:
            result = self.cursor.fetchone() #获取一个结果
            if result != None: #如果查询到结果
                return True #返回true

    #查询单词
    def do_query(self,word):
        sql = "select mean from words where word =%s; "
        self.cursor.execute(sql,[word])
        result = self.cursor.fetchone()#获取一个结果
        if result:#如果有结果就返回结果  返回结果是一个元组
            return result[0]
        else:
            return "not found"
        #将用户表中的id和单词表中的单词id插入到history中

    #用户记录
    def histiry(self,name,word):
        sql = "select id from stu where username =%s; "
        self.cursor.execute(sql, [name])
        use_id = self.cursor.fetchone()[0]
        sql = "insert into(words,user_id)values(%s,%s);"
        try:
            self.cursor.execute(sql, [word,use_id])
            self.db.commit()
        except:
            self.db.rollback()

    def do_history(self,name):
        sql = " select username,words,time from \
              stu inner join history \
                on stu.id = history.user_id \
               where username =%s order by time desc limit 10;"
        self.cursor.execute(sql,[name])
        return self.cursor.fetchall()
