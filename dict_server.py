"""
dict server
"""

from socket import *
from multiprocessing import Process
from signal import *
from dict_data import *
from  time  import sleep


#全局变量
HOST = '0.0.0.0'
PORT = 8887
ADDR = (HOST,PORT)

#调用数据库处理数据
db =DataHaddle()

#用户注册
def do_register(connfd,name,passwd):
    if db.do_register(name,passwd):  # 如果得到结果为真的话，发送“fall”
        connfd.send(b"fall")
    else:
        connfd.send(b"ok")

#用户登录
def do_login(connfd,name,passwd):
    if db.do_login(name,passwd):  # 如果得到结果为真的话，发送“fall”

        connfd.send(b"ok")
    else:
        connfd.send(b"fall")
    print(db.do_login(name,passwd))

#查询单词
def do_query(connfd,name,word):
    db.histiry(name,word) #保存历史记录
    result = db.do_query(word)
    msg =("%s:%s"%(name,result))
    print(result)#打印返回结果
    connfd.send(msg.encode())#将单词解释发送给客户端

#查询历史记录
def do_history(connfd,name):
    result = db.do_history(name) #得到查询结果
    for i in result:#遍历每条结果，中间加sleep是为了防止沾包
       sleep(0.1)
       msg = "%s     %s    %s "% i
       connfd.send(msg.encode())
    connfd.send(b"##")



#客户端连接一个创建一个子进程
def haddle(connfd):
    db.cursor()#为每次连接创建一个游标对象
    while True:
        #接收用户请求
        data = connfd.recv(1024).decode()
        print(data)
        #解析用户请求
        tmp = data.split(" ")
        if tmp[0] =="E" or not data :
            break
        #根据请求发送命令
        elif tmp[0] =="L":
            print(tmp)
            do_register(connfd,tmp[1],tmp[2])
        elif tmp[0] =="R":
            print(tmp)
            do_login(connfd,tmp[1],tmp[2])
        elif tmp[0] =="Q":
            print(tmp)
            if tmp[2] =="##":
                msg ="已结束查询！"
                connfd.send(msg.encode())
                break
            do_query(connfd,tmp[1],tmp[2])
        elif tmp[0] =="H":
            print(tmp)
            do_history(connfd,tmp[1])

    db.cursor.close()
    connfd.close()


#启动函数
def main():
    #建立tcp套接字
    sock = socket()
    sock.bind(ADDR)
    sock.listen(5)
    print("Listen the port %s" % PORT)
    signal(SIGCHLD,SIG_IGN)#回收进程
    while True:
        connfd, addr = sock.accept()#循环创建连接套接字,客户端连接套接字
        print("connet from:",addr)
        p =Process(target=haddle,args=(connfd,))#为客户端连接套接字循环创建子进程
        p.daemon =True #父进程退出，子进程随之退出
        p.start()


if __name__ == '__main__':
    main()