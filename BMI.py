#!/usr/bin/env python3

'''
BMI 指数（即身体质量指数，简称体质指数又称体重，英文为 Body Mass Index，简称BMI），
是用体重公斤数除以身高米数平方得出的数字
'''

print('----欢迎使用BMI计算程序----')
name=input('请键入您的姓名:')
height=eval(input('请键入您的身高(m):'))
weight=eval(input('请键入您的体重(kg):'))
gender=input('请键入你的性别(F/M)')
BMI=float(float(weight)/(float(height)**2))
#公式
if BMI<=18.4:
    print('姓名:',name,'身体状态:偏瘦')
elif BMI<=23.9:
    print('姓名:',name,'身体状态:正常')
elif BMI<=27.9:
    print('姓名:',name,'身体状态:超重')
elif BMI>=28:
    print('姓名:',name,'身体状态:肥胖')
import time;
#time模块
nowtime=(time.asctime(time.localtime(time.time())))
if gender=='F':
    print('感谢',name,'女士在',nowtime,'使用本程序,祝您身体健康!')
if gender=='M':
    print('感谢',name,'先生在',nowtime,'使用本程序,祝您身体健康!')
