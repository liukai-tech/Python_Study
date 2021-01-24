#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
项目名称：使用Python3分析nmea数据文件
版 本 号：V5.0
项目时间：V1.0 by Caesar in 2020/02/10
          V2.0 by Caesar in 2020/02/12
          V3.0 by Caesar in 2020/02/13
          V4.0 by Caesar in 2020/02/20
          V5.0 by Caesar in 2020/02/21
          
功能描述：使用python3分析nmea数据，使用pynmea2进行nmea数据解析，统计GGA总条数，固定比，均值±2cm占比，均值±1cm占比，高程值极差。 -- V1.0 Caesar 2020/02/10
          增加经纬度、米勒投影XY及高程趋势分布图，使用matplotlib绘制，经纬度坐标米勒投影XY坐标系。-- V2.0 Caesar 2020/02/12
          增加使用pyproj进行坐标转换，转换为CGC2000坐标系并绘制XY分布图。-- V3.0 Caesar 2020/02/13
          增加可用卫星颗数、差分延迟趋势图，解状态占比及Avg±2cm Avg±1cm条形图，优化程序结构。 -- V4.0 Caesar 2020/02/20
          增加LLA2ECEF函数，WGS84转地心地固坐标系(ECEF)，优化CGCS2000及LLA2ECEF转换，高程值输入参数为GGA语句内海拔高度与大地水准面高度异常差值之和。 -- V5.0 Caesar 2020/02/21
'''

import pynmea2
import time
import matplotlib.pyplot as plt
import math
from pyproj import CRS, Transformer
import numpy as np


def version():
    print('Version:5.0 by Caesar in 2020/02/21')


cgcs2000_xy = []  #转换后CGCS2000坐标集
xy_coordinate = []  # 转换后的XY坐标集


def millerToXY(lon, lat):
    """
    经纬度转换为平面坐标系中的x,y 利用米勒坐标
    :param lon: 经度
    :param lat: 纬度
    :return:
    """
    L = 6381372 * math.pi * 2
    W = L
    H = L / 2
    mill = 2.3
    x = lon * math.pi / 180
    y = lat * math.pi / 180
    y = 1.25 * math.log(math.tan(0.25 * math.pi + 0.4 * y))
    x = (W / 2) + (W / (2 * math.pi)) * x
    y = (H / 2) - (H / (2 * mill)) * y
    #保留小数点后3位，转换后单位：毫米
    #    xy_coordinate.append((int(round(x)),int(round(y))))
    y *= -1  #y轴反向
    xy_coordinate.append((float(x), float(y)))
    return xy_coordinate


lonlat_coordinate = []  # 经纬度坐标集


def millerToLonLat(x, y):
    """
    将平面坐标系中的x,y转换为经纬度，利用米勒坐标系
    :param x: x轴
    :param y: y轴
    :return:
    """
    L = 6381372 * math.pi * 2
    W = L
    H = L / 2
    mill = 2.3
    lat = ((H / 2 - y) * 2 * mill) / (1.25 * H)
    lat = ((math.atan(math.exp(lat)) - 0.25 * math.pi) * 180) / (0.4 * math.pi)
    lon = (x - W / 2) * 360 / W
    # TODO 最终需要确认经纬度保留小数点后几位
    lonlat_coordinate.append((round(lon, 10), round(lat, 10)))
    return lonlat_coordinate


ecef_xyz = []  #转换后ecef坐标集


def lla2ecef(lat, lon, alt):  #alt为GGA语句内海拔高度与大地水准面高度异常差值之和
    WGS84_A = 6378137.0
    WGS84_f = 1 / 298.257223565
    WGS84_E2 = WGS84_f * (2 - WGS84_f)
    deg2rad = math.pi / 180.0
    rad2deg = 180.0 / math.pi
    lat *= deg2rad
    lon *= deg2rad
    N = WGS84_A / (math.sqrt(1 - WGS84_E2 * math.sin(lat) * math.sin(lat)))
    x = (N + alt) * math.cos(lat) * math.cos(lon)
    y = (N + alt) * math.cos(lat) * math.sin(lon)
    z = (N * (1 - WGS84_f) * (1 - WGS84_f) + alt) * math.sin(lat)
    #ecef_xyz.append((x,y,z))
    return [x, y, z]


def read(filename):
    records = []  #解析列表
    gga_count = [0, 0, 0, 0, 0, 0]  #GGA总数/固定解点数/浮动解点数/差分解点数/单点解点数/未定位点数
    hgts = []  #高程值列表
    hgt_sum = 0.0  #高程累加值
    hgt_min = 0.0  #高程最小值
    hgt_max = 0.0  #高程最大值
    hgt_ud2cm_count = 0  #±2cm数据条数
    hgt_ud1cm_count = 0  #±1cm数据条数
    lat_list = []  #lat列表(有效数据)
    lon_list = []  #lon列表(有效数据)
    sv_list = []  #可用卫星颗数(有效数据)
    diff_delay_list = []  #差分延迟列表(有效数据)

    print('Parse file path:', filename)
    start_time = time.time()

    #使用上下文解析nmea文本数据
    with pynmea2.NMEAFile(filename) as nmea_file:
        for record in nmea_file:
            records.append(record)
            if (record.sentence_type == 'GGA'):  #统计GGA语句条数
                gga_count[0] += 1
                if (record.gps_qual == 4):
                    #if(float(record.age_gps_data) < 20)): #差分延迟小于20秒，累加高程值
                    hgts.append(
                        float(record.altitude) + float(record.geo_sep)
                    )  #将固定解高程值添加至列表(为GGA语句内海拔高度与大地水准面高度异常差值之和)
                    lon_list.append(record.longitude)  #将固定解经度值添加至列表
                    lat_list.append(record.latitude)  #将固定解纬度值添加至列表
                    sv_list.append(int(record.num_sats))  #将固定解可用卫星颗数添加至列表
                    diff_delay_list.append(float(
                        record.age_gps_data))  #将固定解差分延迟添加至列表
                    hgt_sum += (float(record.altitude) + float(record.geo_sep)
                                )  #使用海拔高度+高程异常之和来计算
                    gga_count[1] += 1
                elif (record.gps_qual == 5):  #浮动解
                    gga_count[2] += 1
                elif (record.gps_qual == 2):  #差分解
                    gga_count[3] += 1
                elif (record.gps_qual == 1):  #单点解
                    gga_count[4] += 1
                else:  #未定位
                    gga_count[5] += 1

    end_time = time.time()
    print('Parse used time:%.2f(s)' % (end_time - start_time))

    print('1.Total counts of records:', len(records))

    if gga_count[0] != 0:
        print(
            '2.GGA total counts:%d, Fixed:%d(%.2f%%), Float:%d(%.2f%%), DGPS:%d(%.2f%%), Single:%d(%.2f%%), NoPos:%d(%.2f%%)'
            % (gga_count[0], gga_count[1],
               (gga_count[1] / gga_count[0]) * 100, gga_count[2],
               (gga_count[2] / gga_count[0]) * 100, gga_count[3],
               (gga_count[3] / gga_count[0]) * 100, gga_count[4],
               (gga_count[4] / gga_count[0]) * 100, gga_count[5],
               (gga_count[5] / gga_count[0]) * 100))
    else:
        print('2.Not parsed any GGA sentence')

    if gga_count[1] != 0:
        hgt_avg = hgt_sum / gga_count[1]
        print('3.Hgt average:%.4f(m),' % hgt_avg, end=' ')
        detla_1cm = 0.01
        detla_2cm = 0.02
        for i in range(len(hgts)):
            if (hgts[i] <= hgt_avg + detla_2cm) and (hgts[i] >=
                                                     hgt_avg - detla_2cm):
                hgt_ud2cm_count += 1
            if (hgts[i] <= hgt_avg + detla_1cm) and (hgts[i] >=
                                                     hgt_avg - detla_1cm):
                hgt_ud1cm_count += 1

        print(
            'range ±2cm percent:%.2f(%%), range ±1cm percent:%.2f(%%), max-min:%.4f(m)'
            % ((hgt_ud2cm_count / len(hgts)) * 100,
               (hgt_ud1cm_count / len(hgts)) * 100, max(hgts) - min(hgts)))
    else:
        print('3.Hgt average:Invalid,', end=' ')
        print(
            'range ±2cm percent:Invalid, range ±1cm percent:Invalid, max-min:Invalid'
        )
    '''
    绘制高程值趋势图(实际变化值/平均值/平均值+2cm/平均值-2cm四条曲线)
    '''
    if gga_count[1] != 0:
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

        #WGS84经纬度转米勒投影XY坐标系
        miller_x = []
        miller_y = []
        for i in range(len(lon_list)):
            millerToXY(lon_list[i], lat_list[i])  #经纬度转换为米勒投影坐标xy
            miller_x.append(xy_coordinate[i][0])  #x
            miller_y.append(xy_coordinate[i][1])  #y

        #WGS84经纬度转CGCS2000坐标系
        '''
        Beijing 1954 / Gauss-Kruger CM 117E
        EPSG:21460 with transformation: 15921
        Area of use: China - onshore between 114°E and 120°E
        '''
        cgcs2000_x = []
        cgcs2000_y = []
        transformer = Transformer.from_crs(
            'epsg:4326', 'epsg:4479'
        )  #WGS84转CGCS2000坐标系(epsg:4326为WGS84坐标系编号，epsg:4479为CGCS2000坐标系编号)
        for i in range(len(lon_list)):
            cgc_x, cgc_y, cgc_z = transformer.transform(
                lat_list[i], lon_list[i], hgts[i])
            cgcs2000_xy.append((cgc_x, cgc_y, cgc_z))  #形成多个元组坐标组成的列表
            cgcs2000_x.append(cgc_x)
            cgcs2000_y.append(cgc_y)
        #print('cgcs2000:',cgcs2000_xy) #打印转换后的cgcs2000坐标点集

        #WGS84经纬度转ecef坐标系

        #ecefx0,ecefy0,ecefz0 = lla2ecef(39.0980577883, 117.0814532867, 10.9202)
        #print('\nx:',ecefx0, 'y:',ecefy0, 'z:', ecefz0,'\n')

        ecef_x = []
        ecef_y = []
        for i in range(len(lon_list)):
            ecefx, ecefy, ecefz = lla2ecef(lat_list[i], lon_list[i],
                                           hgts[i])  #经纬度转换为ecef坐标系xyz
            ecef_xyz.append((ecefx, ecefy, ecefz))  #形成多个元组坐标组成的列表
            ecef_x.append(ecefx)  #ecef_x list
            ecef_y.append(ecefy)  #ecef_y list

        #print('\necef:',ecef_xyz) #打印转换后的ecef坐标点集

        x = range(0, len(hgts))
        hgt_y = hgts

        print('gga_count', gga_count)

        GGAPercentN = 5

        percent = [0 for i in range(GGAPercentN)]

        percent[0] = gga_count[1] / gga_count[0]
        percent[1] = gga_count[2] / gga_count[0]
        percent[2] = gga_count[3] / gga_count[0]
        percent[3] = gga_count[4] / gga_count[0]
        percent[4] = gga_count[5] / gga_count[0]

        #print('GGAPercentN',GGAPercentN)

        #绘制解状态占比及Avg±2cm Avg±1cm占比条形图
        fig = plt.figure(num=0)
        #fig.subplots_adjust(bottom=0.025, left=0.025, top = 0.975, right=0.975)
        fig.subplots_adjust(bottom=0.1, left=0.025, top=0.975, right=0.975)
        plt.title('Summary Chart')

        plt.subplot(211)  #1行2列 第1列
        X1 = np.arange(GGAPercentN)
        Y1 = percent * np.ones(GGAPercentN)

        #plt.axes([0.025,0.025,0.95,0.95]) #设置坐标轴
        plt.bar(X1,
                Y1,
                width=0.5,
                facecolor='#9999ff',
                edgecolor='black',
                label='Solution Percent')  #绘制条形码
        plt.legend(loc='upper right')

        solution_text = [
            'Fix(4)', 'Float(5)', 'DGPS(2)', 'Single(1)', 'NoPos(0)'
        ]

        for x1, y1 in zip(X1, Y1):
            plt.text(x1,
                     y1 + 0.1,
                     '%.2f(%%)' % float(y1 * 100.00),
                     ha='center',
                     va='top')  #在对应条形码上方放置条形码数值

        for i in range(GGAPercentN):
            plt.text(i, -0.15, solution_text[i], ha='center',
                     va='bottom')  #在对应条形码下方放置类型

        # 设置横纵坐标上下限及记号
        #plt.xlim(-.5,GGAPercentN), plt.xticks([])
        plt.ylim(-.2, +1.15), plt.yticks([])
        plt.xticks([]), plt.yticks([])

        plt.subplot(212)  #1行2列 第2列

        HgtPercentN = 2

        hgtpercent = [0 for i in range(HgtPercentN)]

        hgtpercent[0] = hgt_ud2cm_count / len(hgts)
        hgtpercent[1] = hgt_ud1cm_count / len(hgts)

        X2 = np.arange(HgtPercentN)
        Y2 = hgtpercent * np.ones(HgtPercentN)

        # plt.axes([0.025,0.025,0.95,0.95]) #设置坐标轴
        plt.bar(X2,
                Y2,
                width=0.3,
                facecolor='#ff9999',
                edgecolor='black',
                label='Avg Percent')  #绘制条形码
        plt.legend(loc='upper right')

        range_text = ['Avg±2cm', 'Avg±1cm']

        for x2, y2 in zip(X2, Y2):
            plt.text(x2,
                     y2 + 0.1,
                     '%.2f(%%)' % float(y2 * 100.00),
                     ha='center',
                     va='top')  #在对应条形码上方放置条形码数值

        for i in range(HgtPercentN):
            plt.text(i, -0.15, range_text[i], ha='center',
                     va='bottom')  #在对应条形码下方放置类型

        plt.text(0.5,
                 0.5,
                 'Max-Min:%.3f(m)' % (max(hgts) - min(hgts)),
                 ha='center',
                 va='top')

        # 设置横纵坐标上下限及记号
        #plt.xlim(-.5,HgtPercentN), plt.xticks([])
        plt.ylim(-.2, +1.15), plt.yticks([])
        plt.xticks([]), plt.yticks([])

        plt.figure(num=1)
        plt.subplot(211)  #2行1列 第1行
        plt.title('Position Chart')
        plt.plot(x,
                 miller_x,
                 linewidth=1.0,
                 color="blue",
                 label='E-W(m)',
                 linestyle=':')  #绘制longitude实际值趋势
        plt.xlabel('Points')
        plt.ylabel('Longitude')
        plt.grid()
        plt.legend()

        plt.subplot(212)  #2行1列 第2行
        plt.plot(x,
                 miller_y,
                 linewidth=1.0,
                 color="red",
                 label='N-S(m)',
                 linestyle=':')  #绘制latitude实际值趋势
        plt.xlabel('Points')
        plt.ylabel('Latitude')
        plt.grid()
        plt.legend()

        plt.figure(num=2)
        plt.title('Height Chart')
        plt.plot(x,
                 hgt_y,
                 linewidth=1.0,
                 color="blue",
                 label='rt hgt',
                 linestyle=':')  #绘制实际值趋势
        plt.plot(x, avg_y, linewidth=1.0, color="green",
                 label='avg hgt')  #绘制平均值直线
        plt.plot(x, u2cm_y, linewidth=1.0, color="red",
                 label='avg+2cm hgt')  #绘制平均值+2cm直线
        plt.plot(x,
                 d2cm_y,
                 linewidth=1.0,
                 color="magenta",
                 label='avg-2cm hgt')  #绘制平均值-2cm直线
        plt.xlabel('Points')
        plt.ylabel('Height(m)')
        plt.grid()
        plt.legend()

        plt.figure(num=3)
        plt.plot(x, sv_list, linewidth=1.0, color="green",
                 linestyle='-')  #绘制可用卫星颗数分布图
        plt.xlabel('Points')
        plt.ylabel('SV')
        plt.title('Satellite In Used Chart')
        plt.grid()

        plt.figure(num=4)
        plt.plot(x, diff_delay_list, linewidth=1.0, color="red",
                 linestyle='-')  #绘制差分延迟分布图
        plt.xlabel('Points')
        plt.ylabel('Diff Age(s)')
        plt.title('Diff Age Chart')
        plt.grid()

        plt.figure(num=5)
        plt.plot(lon_list, lat_list, linewidth=1.0, linestyle=':')  #绘制经纬度分布图
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.xticks(rotation='45')  #x轴标签旋转45度
        plt.title('Lon-Lat Chart')
        plt.grid()

        plt.figure(num=6)
        plt.plot(miller_x, miller_y, linewidth=1.0,
                 linestyle=':')  #绘制米勒投影XY分布图
        plt.xlabel('Miller-X(m)')
        plt.ylabel('Miller-Y(m)')
        plt.title('Miller_XY Chart')
        plt.grid()

        plt.figure(num=7)
        plt.plot(cgcs2000_x, cgcs2000_y, linewidth=1.0,
                 linestyle=':')  #绘制CGCS2000坐标系XY分布图
        plt.xlabel('CGCS2000-X(m)')
        plt.ylabel('CGCS2000-Y(m)')
        plt.title('CGCS2000_XY Chart')
        plt.grid()

        plt.figure(num=8)
        plt.plot(ecef_x, ecef_y, linewidth=1.0, linestyle=':')  #绘制ECEF坐标系XY分布图
        plt.xlabel('ECEF-X(m)')
        plt.ylabel('ECEF-Y(m)')
        plt.title('ECEF_XY Chart')
        plt.grid()

        plt.show()
    else:
        print('4.Data invalid,do not draw plot')


if __name__ == '__main__':
    #    filename = 'H:/python study/gps_line.txt'
    version()  #打印版本号
    filename = 'H:/gps nmea data/bd970_cors_40km_0716.txt'
    read(filename)
