#!/usr/bin/python3
# 文件名：tcp server.py

# 导入 socket、sys 模块
import socket
import sys
import threading
import time

COD = 'utf-8'

def tcplink(sock, addr):
    print('Accept new connection from %s:%s...' % addr)
    sock.send(('Welcome').encode(COD))
    while True:
        data = sock.recv(1024)
        time.sleep(1)
        if data.decode(COD) == 'exit':
            break    
        print('{0} recv: {1} ,count: {2}' .format(addr, data.decode(COD), len(data.decode(COD))))
        sock.send(data)
    sock.close()
    print('Connection from %s:%s closed.' % addr)


# 创建 socket 对象
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

address = ('127.0.0.1', 9999)

# 监听端口
s.bind(address)

# 设置最大等待数
s.listen(5)

print('Waiting for connection...')

while True:
    # 接受一个新连接:
    sock, addr = s.accept()

    # 创建新线程来处理TCP连接:
    t = threading.Thread(target=tcplink, args=(sock, addr))
    t.start()
