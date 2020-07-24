"""
在线词典  client
"""
from socket import *
import re
from time import sleep

# 服务器地址
HOST = '127.0.0.1'
PORT = 8887
ADDR = (HOST,PORT)

#菜单1
def menu1():
    print(
        """
        =========选择功能==========
        1 登录
        2 注册
        3 退出
        ==========================
        """
    )

def menu2():
    print(
        """
        =========选择功能==========
        1 查询单词
        2 历史记录
        3 注销
        ==========================
        """
    )

#用户注册
def do_register(sock):
    name =input("请输入用户名：")
    password = input("请输入密码：")
    password_aegin = input("请再次输入密码：")
    if password != password_aegin or " " in password or " " in name:
        print("密码输入错误,请重新输入")
        menu1()
    msg =("L %s %s"%(name,password))
    sock.send(msg.encode())
    result = sock.recv(1024).decode()
    print(result)
    if result =="ok":
        print("注册成功,请重新登录")
        menu1()
    else:
        print("用户已存在！,请重新输入")
        menu1()

#用户登录
def do_login(sock):
    name =input("请输入用户名：")
    password = input("请输入密码：")
    msg =("R %s %s"%(name,password))
    sock.send(msg.encode())#发送消息给服务端
    result = sock.recv(1024).decode()#接收服务端消息
    print(result)
    if result =="ok":
        secend_menu(sock,name) #name 重这边获取

    else:
        print("用户名或者密码输入错误，请重新登录！")
        menu1()

#查询单词
def do_query(sock,name):
    while True:
        words = input("请输入单词：")
        msg =("Q %s %s"%(name,words))
        sock.send(msg.encode())#向服务端发送请求
        data = sock.recv(1024)
        print(data.decode())#接手服务端请求
        if words =="##":
            return

#查询历史记录
def do_history(sock,name):
    msg ="H "+name
    sock.send(msg.encode())#发送给服务端消息
    while True:
        sleep(0.1)
        data = sock.recv(1024).decode()
        print(data)
        if data =="##":#收到##后表示接受完毕
            break
        return






#一级菜单功能
def first_menu(sock):
    menu1()
    while True:
        option = input("请选择命令：")
        cmd =re.sub("\D","",option)
        if  cmd in ["1","2","3"]:
            if cmd == "1":# print("登录")
                do_login(sock)
            elif cmd == "2": # print("注册")
                do_register(sock)
            elif cmd == "3":
                sock.send(b"E")
                print("您已退出程序")
                break
        else:
            print("您输入命令错误,请输入1、2 or 3")
        break
    sock.close()

#二级菜单功能
def secend_menu(sock,name):
    menu2()
    while True:
        option = input("请选择命令：")
        cmd = re.sub("\D", "", option)
        if cmd in ["1", "2", "3"]:
            if cmd == "1": #print("查询单词")
                do_query(sock,name)
                menu2()
            elif cmd == "2":#print("历史记录")
                do_history(sock, name)
            elif cmd == "3":
                first_menu(sock)#进入一级菜单功能
                break
        else:
            print("您输入命令错误,请输入1、2 or 3")


#启动函数
def main():
    sock =socket()
    #建立连接
    sock.connect(ADDR)
    first_menu(sock)



if __name__ == '__main__':
    main()




