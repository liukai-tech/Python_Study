# -----------------------------------------------------------------------------
# Copyright (c) 2015, Nicolas P. Rougier. All Rights Reserved.
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------

#!/usr/bin/env python3

#等高线图

import numpy as np
import matplotlib.pyplot as plt

def f(x,y):
    return (1-x/2+x**5+y**3)*np.exp(-x**2-y**2)

n = 256
x = np.linspace(-3,3,n)
y = np.linspace(-3,3,n)
X,Y = np.meshgrid(x,y) #从坐标向量返回坐标矩阵

plt.axes([0.025,0.025,0.95,0.95]) #设置坐标轴

#plt.contourf(X, Y, f(X,Y), 8, alpha=.75, cmap=plt.cm.hot)
plt.contourf(X, Y, f(X, Y), 8, alpha=.75, cmap='jet') #绘制轮廓
C = plt.contour(X, Y, f(X,Y), 8, colors='black', linewidths=.5) #绘制等高线
plt.clabel(C, inline=1, fontsize=10) #标记等高线图

plt.xticks([]), plt.yticks([])
#plt.savefig('./contour_ex.png',dpi=72)# 以分辨率 72 来保存图片
plt.show()
