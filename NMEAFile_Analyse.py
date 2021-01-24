#!/usr/bin/python3
# encoding: utf-8

#Version:1.0 by Caesar in 2/10 2020

#功能：使用python3分析nmea数据，统计GGA总条数，固定比，均值±2cm占比，均值±1cm占比，高程值极差

import pynmea2
import time

def read(filename):
    records = []        #解析列表
    gga_sumcount = 0    #gga语句总统计值
    gga_validcount = 0  #gga有效语句统计值（固定且差分延迟小于20秒）
    hgts = []           #高程值列表
    hgt_sum = 0.0       #高程累加值
    hgt_min = 0.0       #高程最小值
    hgt_max = 0.0       #高程最大值
    hgt_ud2cm_count = 0 #±2cm数据条数
    hgt_ud1cm_count = 0 #±1cm数据条数

    print('Parse file path:',filename)
    start_time = time.time()
    
    with pynmea2.NMEAFile(filename) as nmea_file:
        for record in nmea_file:
            records.append(record)
            if(record.sentence_type == 'GGA'):#统计GGA语句条数
                gga_sumcount += 1
                if((record.gps_qual == 4) and (float(record.age_gps_data) < 20)):#固定解且差分延迟小于20秒，累加高程值
                    hgts.append(float(record.altitude))#将固定解高程值添加至列表
                    hgt_sum += float(record.altitude)
                    gga_validcount += 1
                   
    end_time = time.time()
    print('Parse used time:%.2f(s)' % (end_time - start_time))
    
    print('1.Total counts of records:', len(records))

    print('2.GGA total counts: %d, fixed counts: %d, fixed percent:%.2f(%%)' % (gga_sumcount, gga_validcount, (gga_validcount / gga_sumcount)*100 ))

    if gga_validcount != 0:
        hgt_avg = hgt_sum / gga_validcount
        print('3.Hgt average:%.4f(m),' % hgt_avg, end = ' ')
        detla_1cm = 0.01
        detla_2cm = 0.02
        for i in range(len(hgts)):
            if (hgts[i] <= hgt_avg + detla_2cm) and (hgts[i] >= hgt_avg - detla_2cm):
                hgt_ud2cm_count += 1
            if (hgts[i] <= hgt_avg + detla_1cm) and (hgts[i] >= hgt_avg - detla_1cm):
                hgt_ud1cm_count += 1  
    else:
        print('3.Hgt average:Invalid,' , end = ' ')

    if len(hgts) != 0:
        print('range ±2cm percent:%.2f(%%), range ±1cm percent:%.2f(%%), max-min:%.4f(m)' % ((hgt_ud2cm_count / len(hgts)) * 100, (hgt_ud1cm_count / len(hgts)) * 100, max(hgts) - min(hgts)))
    else:
        print('range ±2cm percent:Invalid, range ±1cm percent:Invalid, max-min:Invalid')

#    print('3.Hgt average:%.4f(m), range ±2cm percent:%.2f(%%), max-min:%.4f(m)' % (hgt_avg, percent_2cm * 100, max_min))

if __name__ == '__main__':
#    filename = 'H:/python study/gps_line.txt'
    filename = 'H:/gps nmea data/bd970_cors_40km.txt'
    read(filename)
