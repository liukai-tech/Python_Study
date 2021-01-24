#!/usr/bin/python3
# 文件名：server.py
 
# 导入 socket、sys 模块
import socket
import sys
 
# 创建 socket 对象
serversocket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
 
# 获取本地主机名
host = socket.gethostname()
 
port = 9999

address = ('127.0.0.1', 9999)
 
# 绑定端口
serversocket.bind(address)
 
# 设置最大连接数，超过后排队
serversocket.listen(5)
 
while True:
    # 建立客户端连接
    clientsocket,addr = serversocket.accept()     
 
    print("got connected from: %s" % str(addr))
     
    msg='Welcome to visit Caesar\'s website'+ "\r\n"
    clientsocket.send(msg.encode('utf-8'))
    #clientsocket.close()
