#!/usr/bin/python3
# 文件名：ntripclient.py

# ntrip客户端

import socket   # 导入 socket 模块
import base64   # 导入 base64 模块
import time     # 导入 time 模块
from threading import Thread  # 导入 threading 模块
import serial   # 导入 serial 模块

COD = 'ascii'

gpggaSentence = "$GPGGA,072034.00,3905.8186042,N,11704.9435945,E,4,18,0.8,1.6436,M,-8.922,M,01,0004*4B\r\n"

host = '39.100.152.105'  # host for the service
port = 50005  # port for the service
username = '123'  # username for RTCM correction service
password = '123'  # password for RTCM correction service
mountpoint = 'RTCM32'  # mountpoint
'''Generate an encoding of the username:password for the service.
The string must be first encoded in ascii to be correctly parsed by the
base64.b64encode function.'''
pwd = base64.b64encode("{}:{}".format(username, password).encode(COD))

# The following decoding is necessary in order to remove the b' character that
# the ascii encoding add. Othrewise said character will be sent to the net and misinterpreted.
pwd = pwd.decode(COD)

# construction get rtcm stream header
getRTCMStreamHeader =\
"GET /{} HTTP/1.1\r\n".format(mountpoint) +\
"Ntrip-Version: Ntrip/1.0\r\n" +\
"User-Agent: ntrip.py/0.1\r\n" +\
"Accept: */*" +\
"Connection: close\r\n" +\
"Authorization: Basic {}\r\n\r\n".format(pwd)

#windows
serialname = 'COM1'

#linux
#serialname = '/dev/ttymxc2'


com = None

def message_handle(client):
    '''
    消息处理
    '''
    check_icy200ok_flag = False
    icy200ok_str = 'ICY 200 OK'

    while True:
        try:
            if check_icy200ok_flag is False:
                time.sleep(0.1)
                print(getRTCMStreamHeader)
                client.sendall(getRTCMStreamHeader.encode(COD))
            else:
                client.sendall(gpggaSentence.encode(COD))
                time.sleep(0.5)

            rxbytes = client.recv(1024)  # 阻塞接收数据
            if check_icy200ok_flag is False:
                if icy200ok_str.encode(COD) in rxbytes:
                    check_icy200ok_flag = True
                    print('Recv server msg:ICY 200 OK, len:{}'.format(
                        len(rxbytes)))
                else:
                    pass
            else:
                if len(rxbytes) > 0 and rxbytes[0] == 0xd3:  # 收到差分数据
                    print('Recv rtcm stream, len:{}'.format(len(rxbytes)))
                    wdsize = com.write(rxbytes)
                    print('Send to serial port {0}, len:{1}'.format(serialname, wdsize))
                else:
                    pass

        except ConnectionAbortedError:  # 服务器中止连接，关闭socket
            print('Remote server Connect Aborted.')
            client.close()
            break


if __name__ == '__main__':

    while True:
        if com is None:
            try:
                com = serial.Serial(serialname, baudrate=115200, timeout=5.0) # 打开serial port
                break
            except serial.SerialException:
                print('could not connect to %s' % serialname)
                time.sleep(5.0)
                continue
    sock = socket.socket()  # 创建 socket 对象
    sock.connect((host, int(port)))  # 连接server
    print('Connect ok.')
    thread = Thread(target=message_handle,
                    args=(sock, ))  # 创建一个独立的线程进行消息处理(只传入socket句柄，忽略addr)
    thread.setDaemon(True)  # 设置成守护进程
    thread.start()  # 开启线程

    # 主线程逻辑(控制台输入数据进行发送)
    while True:
        cmd = input("")
        try:
            sock.sendall(cmd.encode(COD))
        except OSError:
            print('Server closed,exit.')
            sock.close()
            exit()
