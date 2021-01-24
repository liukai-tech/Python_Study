#!/usr/bin/python3
# 文件名：server_threading.py

# 多线程socket服务器

'''
1.新开一个线程用于接收新的连接(socket.accept())
2.当有新的连接时，再新开一个线程，用于接收这个连接的消息(socket.recv())
3.主线程作为控制台，接收用户的输入，进行其他操作。
'''

import socket                   # 导入socket模块
from threading import Thread    # 导入 threading 模块
import sys

ADDRESS = ('127.0.0.1', 9999)  # 绑定地址

g_socket_server = None  # 负责监听的socket

g_conn_pool = []  # 连接池(socket句柄)
g_conn_addr = []  # IP地址连接池(ipaddr)


def init():
    '''
    初始化服务端
    '''
    global g_socket_server
    g_socket_server = socket.socket(socket.AF_INET,
                                    socket.SOCK_STREAM)  # 创建socket对象
    g_socket_server.bind(ADDRESS)  # 监听端口
    g_socket_server.listen(5)  # 最大等待数（不要误理解为最大连接数）
    print('Server socket start,wait client connect...')


def accept_client():
    '''
    接受新连接
    '''
    while True:
        client, addr = g_socket_server.accept()  # 阻塞，等待客户端连接
        print('Client {} gets online.'.format(addr))    # 打印client上线
        g_conn_pool.append(client)  # 加入连接池
        g_conn_addr.append(addr)    # 加入IP地址连接池
        thread = Thread(target=message_handle,
                        args=(client, ))  # 给每个客户端创建一个独立的线程进行管理(只传入client句柄，忽略addr)
        thread.setDaemon(True)  # 设置成守护进程
        thread.start()  # 开启线程


def message_handle(client):
    '''
    消息处理
    '''
    client.sendall("Connect server successful!".encode(encoding='utf8'))
    while True:
        try:
            rxbytes = client.recv(1024)     # 阻塞接收数据      
            if len(rxbytes) == 0:           # 接收到数据长度为0，判断client已断开，处理相关句柄
                client.close()
                index = g_conn_pool.index(client)       # 获取索引位置
                addr = g_conn_addr[index]               # 获取IP地址
                g_conn_pool.remove(client)              # 删除连接
                g_conn_addr.remove(g_conn_addr[index])  # 删除IP地址
                print("Index:{0}, addr:{1} client disconnect.".format(index, addr))
                break
            else:
                print('Recv client msg:{0}, len:{1}'.format(rxbytes.decode(encoding='utf8'), len(rxbytes.decode(encoding='utf8'))))
                client.sendall(rxbytes)  # 回显数据
        except ConnectionResetError:    # 客户端主动断开连接,更新连接池
            client.close()
            index = g_conn_pool.index(client)       # 获取索引位置
            addr = g_conn_addr[index]               # 获取IP地址
            g_conn_pool.remove(client)              # 删除连接
            g_conn_addr.remove(g_conn_addr[index])  # 删除IP地址
            print("Index:{0}, addr:{1} client disconnect.".format(index, addr))
            break


if __name__ == '__main__':
    init()
    # 新开一个线程，用于接收新连接
    thread = Thread(target=accept_client)
    thread.setDaemon(True)
    thread.start()

    # 主线程逻辑
    while True:
        try:
            cmd = input('''----------------------------
Enter 1:Check online client number.
Enter 2:Send msg to client.
Enter 3:Close server.\n''')

            if cmd == '1':
                print('----------------------------')
                print('Online client number:', len(g_conn_pool))
                for i in range(0, len(g_conn_addr)):
                    print('index:{0}, addr:{1}'.format(i, g_conn_addr[i]))

            elif cmd == '2':
                print('----------------------------')
                index, msg = input('Please enter \'index, msg\' type(index start in 0):').split(',')
                if (int(index) < len(g_conn_pool)):
                    g_conn_pool[int(index)].sendall(msg.encode(encoding='utf8'))
                else:
                    print('Error,index out of range.')
                    pass

            elif cmd == '3':
                print('Server closed.')
                sys.exit()       
        except KeyboardInterrupt:
            sys.exit()
