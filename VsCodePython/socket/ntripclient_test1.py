#!/usr/bin/python3
# 文件名：ntripclient.py

# ntrip客户端
'''
1.连接服务器成功后新开一个线程用于接收消息处理(socket.recv())
2.主线程作为控制台，接收用户的输入，发送数据至服务器。
'''

import socket  # 导入 socket 模块
from threading import Thread  # 导入 threading 模块
import time

ADDRESS = ('39.100.152.105', 50005)

getSrcTable = 'GET / HTTP/1.0\r\n\
User-Agent: NTRIP SunNav NtripClient/1.2\r\n\
Accept: */*\r\n\
Connection: close\n\n\
\r\n\r\n'

getRTCMStream = '\
GET /RTCM32 HTTP/1.0\r\n\
User-Agent: NTRIP SunNav NtripClient/1.2\r\n\
Accept: */*\r\n\
Authorization: Basic MTIzOjEyMw==\n\
\r\n\r\n'

gpggaSentence = '$GPGGA,072034.00,3905.8186042,N,11704.9435945,E,4,18,0.8,1.6436,M,-8.922,M,01,0004*4B\r\n'


def message_handle(client):
    '''
    消息处理
    '''
    check_icy200ok_flag = False

    while True:
        try:
            if check_icy200ok_flag is False:
                time.sleep(0.1)
                print(getRTCMStream)
                client.sendall(getRTCMStream.encode(encoding='utf8'))
            else:
                client.sendall(gpggaSentence.encode(encoding='utf8'))
                time.sleep(0.5)

            rxbytes = client.recv(1024)  # 阻塞接收数据
            if rxbytes[0] == 0xd3:  # 收到差分数据
                print('Recv rtcm stream, len:{}'.format(len(rxbytes)))
            else:
                if check_icy200ok_flag is False:
                    rxstr = rxbytes.decode(encoding='utf8')
                    if 'ICY 200 OK' in rxstr:
                        check_icy200ok_flag = True
                    print('Recv server msg:{0}, len:{1}'.format(
                        rxstr, len(rxstr)))
                else:
                    print('Recv rtcm stream, len:{}'.format(len(rxbytes)))
        except ConnectionAbortedError:  # 服务器中止连接，关闭socket
            print('Remote server Connect Aborted.')
            client.close()
            break


if __name__ == '__main__':
    sock = socket.socket()  # 创建 socket 对象
    sock.connect(ADDRESS)  # 连接server
    print('Connect ok.')
    #   sock.sendall(getSrcTable.encode(encoding='utf8'))
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
