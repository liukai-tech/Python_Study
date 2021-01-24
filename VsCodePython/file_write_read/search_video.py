#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

'''
输入指定目录，扫描此目录下所有目标格式文件，并将地址存储到txt文件中
支持类型：video/picture/voice/text
下一步考虑输入单个目录，多线程同时搜索指定类型的文件。
Code by Caesar in 2020/03/05
'''

import os
import time

def search_file(start_dir, target):
    os.chdir(start_dir)  # 改变当前工作目录至用户输入目录

    for each_file in os.listdir(os.curdir):
        ext = os.path.splitext(each_file)[1]  # 分解文件名得到后缀名
        if ext in target:   # 判断后缀名是否符合目标
            targetfile_list.append(os.getcwd() + os.sep + each_file + os.linesep)  # 将符合目标的文件目录添加至列表中
        if os.path.isdir(each_file):    # 如果当前文件是目录
            search_file(each_file, target)  # 递归调用
            os.chdir(os.pardir)  # 递归调用后切记返回上一层目录

# 选择待查找的文件类型
# video type
targetOrgin = ['.3GP', '.AVI', '.MP4', '.RMVB', '.MOV', '.RM', '.FLV', '.QT', '.ASF', '.MPEG', '.MPG', '.WMV']

# picture type
# targetOrgin = ['.BMP', '.JPG', '.JPEG', '.PNG', '.GIF', '.PSD', '.PDD', '.DXF', '.WMF', '.EMF', '.FLC', '.FLI', '.SVG', '.PCX', '.EPS', '.TGA']

# voice type
#targetOrgin = ['.MP3', '.AAC', '.WAV', '.WMA', '.CDA', '.FLAC', '.M4A', '.MID', '.MKA', '.MP2', '.MPA', '.MPC',\
#'.APE', '.OFR', '.OGG', '.RA', '.WV', '.TTA', '.AC3', '.DTS', '.AU', '.MMF']

# text type
# targetOrgin = ['.TXT', '.DOC', '.DOCX', '.XLS', '.XLSX', '.HLP', '.WPS', '.RTF', '.HTML', '.PDF']

target = [x.lower() for x in targetOrgin if isinstance(x, str)]     # 采用列表式将大写后缀名转为小写
target.extend(targetOrgin)  # 将原有大写后缀名添加进来

# 批量生成测试文件(根据不同类型修改测试目录)
'''
filepath = 'H:/tmp/text'

for x in targetOrgin:
    path = filepath + os.sep + '1234' + x
    try:
        fd = open(path, 'w')
    finally:
        fd.close

    path = filepath + os.sep + '123' + x.lower()
    try:
        fd = open(path, 'w')
    finally:
        fd.close    
'''            

start_dir = input('Please enter the initial directory to find：')
print('Start search files.')
start_time = time.time()
program_dir = os.getcwd()

targetfile_list = []

# 根据待查找的文件类型确定存储文件名
targetfilename = 'videoList.txt'
# targetfilename = 'picList.txt'
# targetfilename = 'voiceList.txt'
# targetfilename = 'textList.txt'

search_file(start_dir, target)

f = open(program_dir + os.sep + targetfilename, 'w')
f.writelines(targetfile_list)
f.close()

end_time = time.time()
print('Search file finished, total used time {:.2f} sec.'.format(end_time - start_time))
print('Search results are stored in {}'.format(program_dir + os.sep + targetfilename))
