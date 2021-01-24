#!/usr/bin/python3

# 检索指定路径下后缀是 py 的所有文件

import os
import os.path

# path = 'H:/'
ls = []


def getAppointFile(path, ls):
    fileList = os.listdir(path)
    try:
        for tmp in fileList:
            pathTmp = os.path.join(path, tmp)
            if os.path.isdir(pathTmp):
                getAppointFile(pathTmp, ls)
            elif pathTmp[pathTmp.rfind('.') + 1:].upper() == 'PY':
                ls.append(pathTmp)
    except PermissionError:
        pass


def main():

    while True:
        path = input('Please enter path:').strip()
        if os.path.isdir(path):  # 存在此路径
            break

    getAppointFile(path, ls)
    # print(len(ls))
    print(ls)
    print(len(ls))


main()
