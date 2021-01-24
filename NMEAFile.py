#! /usr/bin/env python3

#使用pynmea2库对nmea数据文件进行解析,然后打印每一条数据.

'''
参考网址：http://gnss.help/2018/03/01/pynmea2-readme/index.html

1.安装pynmea2模块
    pip install pynmea2
2.导入pynmea2
    import pynmea2
3.使用NMEAFile()解析文件

修改文件目录('H:/python study/gps_line.txt')即可解析不同NMEA文件
'''


import pynmea2

records = []

nmeafilepath = 'H:/python study/gps_line.txt'

with pynmea2.NMEAFile(nmeafilepath) as nmea_file:
    for record in nmea_file:
        records.append(record)

print('Parse nmea file path:',nmeafilepath)

print('Count of records:', len(records))

for i in range(len(records)):
    print('\n%d nmea sentence:' % i)
    print(repr(records[i]))

