#!/usr/bin/python3
# 文件名：client_threading.py

# 多线程socket客户端
'''
1.连接服务器成功后新开一个线程用于接收消息处理(socket.recv())
2.主线程作为控制台，接收用户的输入，发送数据至服务器。
'''

import socket  # 导入 socket 模块
from threading import Thread  # 导入 threading 模块

ADDRESS = ('127.0.0.1', 9999)


def message_handle(client):
    '''
    消息处理
    '''
    while True:
        try:
            rxbytes = client.recv(1024)  # 阻塞接收数据
            if len(rxbytes) == 0:  # 接收到数据长度为0，判断server已关闭，关闭socket
                client.close()
                break
            else:
                print('Recv server msg:{0}, len:{1}'.format(
                    rxbytes.decode(encoding='utf8'),
                    len(rxbytes.decode(encoding='utf8'))))
        except ConnectionResetError:  # 服务器断开，关闭socket
            client.close()
            break


if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建socket对象
    sock.connect(ADDRESS)  # 连接server
    print('Connect ok.')
    thread = Thread(target=message_handle,
                    args=(sock, ))  # 创建一个独立的线程进行消息处理(只传入socket句柄，忽略addr)
    thread.setDaemon(True)  # 设置成守护进程
    thread.start()  # 开启线程

    # 主线程逻辑(控制台输入数据进行发送)
    while True:
        cmd = input("")
        try:
            sock.sendall(cmd.encode(encoding='utf8'))
        except OSError:
            print('Server closed,exit.')
            sock.close()
            exit()
