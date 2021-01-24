#!/usr/bin/python3

# 操作系统接口
import os
print('Current working directory:{}'.format(os.getcwd()))  # 返回当前的工作目录

# 文件通配符
# glob模块提供了一个函数用于从目录通配符搜索中生成文件列表:
import glob
print('sreach file list:{}'.format(repr(glob.glob('*.py'))))

# 字符串正则匹配
# re模块为高级字符串处理提供了正则表达式工具。对于复杂的匹配和处理，正则表达式提供了简洁、优化的解决方案:
import re
print(re.findall(r'\bf[a-z]*', 'which foot or hand fell fastest'))

print(re.sub(r'(\b[a-z]+) \1', r'\1', 'cat in the the hat'))

# 数学
# math模块为浮点运算提供了对底层C函数库的访问:
import math
print('math.cos results:{}'.format(math.cos(math.pi / 4)))
print('math.log results:{}'.format(math.log(1024, 2)))

# random提供了生成随机数的工具。
import random
print('random.choice results:{}'.format(random.choice(['apple', 'pear', 'banana'])))
print('random.sample results:{}'.format(random.sample(range(100), 10)))   # sampling without replacement
print('random.random results:{}'.format(random.random()))    # random float
print('random.randrange results:{}'.format(random.randrange(6)))    # random integer chosen from range(6)

# 访问 互联网
# 有几个模块用于访问互联网以及处理网络通信协议。其中最简单的两个是用于处理从 urls 接收的数据的 urllib.request 以及用于发送电子邮件的 smtplib:
'''
from urllib.request import urlopen
for line in urlopen('http://tycho.usno.navy.mil/cgi-bin/timer.pl'):
    line = line.decode('utf-8')  # Decoding the binary data to text.
    if 'EST' in line or 'EDT' in line:  # look for Eastern Time
        print(line)
'''
# smtplib例子见smtp文件夹

# 日期和时间
# datetime模块为日期和时间处理同时提供了简单和复杂的方法。

# 支持日期和时间算法的同时，实现的重点放在更有效的处理和格式化输出。

# 该模块还支持时区处理:

# dates are easily constructed and formatted
import datetime
now = datetime.date.today()
print('date now:{}'.format(now))
print(now.strftime("%m-%d-%y. %d %b %Y is a %A on the %d day of %B."))

# dates support calendar arithmetic
birthday = datetime.date(1994, 5, 4)
age = now - birthday
print(age.days)

# 常用时间处理方法

today = datetime.date.today()   # 今天
print('today:{}'.format(today))
yesterday = today - datetime.timedelta(days=1)  # 昨天 
print('yesterday:{}'.format(yesterday))
last_month = today.month - 1 if today.month - 1 else 12 # 上个月 
print('last_month:{}'.format(last_month))
print('isocalendar:{}'.format(datetime.date.isocalendar(today)))
#time_stamp = datetime.time.time()    # 当前时间戳 
#print('time_stamp:{}'.format(time_stamp))
#print('时间戳转datetime:{}'.format(datetime.datetime.fromtimestamp(time_stamp))  # 时间戳转datetime

print('ISO标准日期字符串:{}'.format(today.isoformat()))    #datetime转字符串
today_str = today.strftime('%Y-%m-%d')
print('datetime转字符串:{}'.format(today_str))    #datetime转字符串  
print('字符串转datetime:{}'.format(datetime.datetime.strptime(today_str, "%Y-%m-%d")))# 字符串转datetime 
print('补时差:{}'.format(today + datetime.timedelta(hours=8)))  # 补时差 

# 数据压缩
# 以下模块直接支持通用的数据打包和压缩格式：zlib，gzip，bz2，zipfile，以及 tarfile。

import zlib
s = b'witch which has which witches wrist watch'
print('s len:{}'.format(len(s)))
t = zlib.compress(s)
print('t len:{}'.format(len(t)))
print('t decompress:{}'.format(zlib.decompress(t)))
print('s crc32:{}'.format(zlib.crc32(s)))

