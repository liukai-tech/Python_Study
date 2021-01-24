#!/usr/bin/python3
# -*- encoding: utf-8 -*-

'''
项目名称：使用Python3分析nmea数据文件
版 本 号：V2.0
项目时间：V1.0 by Caesar in 2020/02/10
          V2.0 by Caesar in 2020/02/12
功能描述：使用python3分析nmea数据，使用pynmea2进行nmea数据解析，统计GGA总条数，固定比，均值±2cm占比，均值±1cm占比，高程值极差。 -- V1.0 Caesar 2020/02/10
          增加经纬度、米勒投影XY及高程趋势分布图，使用matplotlib绘制，经纬度坐标米勒投影XY坐标系。-- V2.0 Caesar 2020/02/12
          
'''

import pynmea2
import time
import matplotlib.pyplot as plt
import math

def version():
    print('Version:2.0 by Caesar in 2020/02/12')

xy_coordinate = [] # 转换后的XY坐标集
def millerToXY (lon, lat):
    """
    经纬度转换为平面坐标系中的x,y 利用米勒坐标
    :param lon: 经度
    :param lat: 纬度
    :return:
    """
    L = 6381372*math.pi*2
    W = L
    H = L/2
    mill = 2.3
    x = lon*math.pi/180
    y = lat*math.pi/180
    y = 1.25*math.log(math.tan(0.25*math.pi+0.4*y))
    x = (W/2)+(W/(2*math.pi))*x
    y = (H/2)-(H/(2*mill))*y
    #保留小数点后3位，转换后单位：毫米
#    xy_coordinate.append((int(round(x)),int(round(y))))
    y *= -1 #y轴反向
    xy_coordinate.append((float(x),float(y)))
    return xy_coordinate

lonlat_coordinate = [] # 经纬度坐标集
def millerToLonLat(x, y):
    """
    将平面坐标系中的x,y转换为经纬度，利用米勒坐标系
    :param x: x轴
    :param y: y轴
    :return:
    """
    L = 6381372 * math.pi*2
    W = L
    H = L/2
    mill = 2.3
    lat = ((H/2-y)*2*mill)/(1.25*H)
    lat = ((math.atan(math.exp(lat))-0.25*math.pi)*180)/(0.4*math.pi)
    lon = (x-W/2)*360/W
    # TODO 最终需要确认经纬度保留小数点后几位
    lonlat_coordinate.append((round(lon,10),round(lat,10)))
    return lonlat_coordinate 

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
    lat_list = []       #lat列表(有效数据)
    lon_list = []       #lon列表(有效数据)

    print('Parse file path:',filename)
    start_time = time.time()

    #使用上下文解析nmea文本数据
    with pynmea2.NMEAFile(filename) as nmea_file:
        for record in nmea_file:
            records.append(record)
            if(record.sentence_type == 'GGA'):#统计GGA语句条数
                gga_sumcount += 1
                if((record.gps_qual == 4) and (float(record.age_gps_data) < 20)):#固定解且差分延迟小于20秒，累加高程值
                    hgts.append(float(record.altitude))#将固定解高程值添加至列表
                    lon_list.append(record.longitude)#将固定解经度值添加至列表
                    lat_list.append(record.latitude)#将固定解纬度值添加至列表                   
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

    '''
    绘制高程值趋势图(实际变化值/平均值/平均值+2cm/平均值-2cm四条曲线)
    '''
    if (gga_validcount != 0) and (len(hgts) != 0):
        print('4.Draw plot')
        hgt_avg_list = []
        hgt_u2cm_list = []
        hgt_d2cm_list = []
        for i in range(len(hgts)):
            hgt_avg_list.append(hgt_avg)
            hgt_u2cm_list.append(hgt_avg + detla_2cm)
            hgt_d2cm_list.append(hgt_avg - detla_2cm)
            
        avg_y = hgt_avg_list
        u2cm_y = hgt_u2cm_list
        d2cm_y = hgt_d2cm_list

        miller_x = []
        miller_y = []
        for i in range(len(lon_list)):
            millerToXY(lon_list[i], lat_list[i])#经纬度转换为米勒投影坐标xy
            miller_x.append(xy_coordinate[i][0])#x
            miller_y.append(xy_coordinate[i][1])#y

        x = range(0,len(hgts))
        hgt_y = hgts
        plt.figure(num=1)
        plt.plot(x,hgt_y)#绘制实际值趋势
        plt.plot(x,avg_y)#绘制平均值直线
        plt.plot(x,u2cm_y)#绘制平均值+2cm直线
        plt.plot(x,d2cm_y)#绘制平均值-2cm直线
        plt.figure(num=2)
        plt.plot(lon_list,lat_list)#绘制经纬度分布图
        plt.figure(num=3)
        plt.plot(miller_x,miller_y)#绘制XY分布图
        plt.show()
    else:
        print('4.Data invalid,do not draw plot')

if __name__ == '__main__':
#    filename = 'H:/python study/gps_line.txt'
    version()#打印版本号
    filename = 'H:/gps nmea data/bd970_cors_40km_0716.txt'
    read(filename)
