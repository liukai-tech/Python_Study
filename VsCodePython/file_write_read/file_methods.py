#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

'''
由于文件读写时都有可能产生 IOError，一旦出错，后面的 f.close() 就不会调用。
所以，为了保证无论是否出错都能正确的关闭文件，可以使用 try...finally 来实现：
'''

gga = '$GPGGA,072403.40,3905.8167128,N,11704.9465486,E,4,18,0.8,1.5930,M,-8.921,M,00,0004*40\n'

# 写入数据
try:
    f = open('H:/python study/VsCodePython/file_write_read/file_test1.txt', 'a+')
    wsize = f.write(gga)
    print('Write Size:', wsize)
finally:
    if f:
        f.close()

# 读取数据
try:
    # f = open('H:/python study/VsCodePython/file_write_read/file_test1.txt', 'r') # mode=r时为只读，然后文件指针在0，可以正常读取;
    f = open('H:/python study/VsCodePython/file_write_read/file_test1.txt', 'a+')  # mode=a+时，属于在文件后继续添加内容，此时读取需要将文件指针移动到0处(f.seek(0));
    f.seek(0)  # 移动文件指针到0处开始读取数据
    for line in f:
        print('read size:', len(line), 'data:', line, end='')
finally:
    if f:
        f.close()
