# -----------------------------------------------------------------------------
# Copyright (c) 2015, Nicolas P. Rougier. All Rights Reserved.
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------

#!/usr/bin/env python3

#灰度图

import numpy as np
import matplotlib.pyplot as plt

def f(x,y):
    return (1-x/2+x**5+y**3)*np.exp(-x**2-y**2)

n = 10
x = np.linspace(-3,3,int(3.5*n))
y = np.linspace(-3,3,int(3.0*n))
X,Y = np.meshgrid(x,y)
Z = f(X,Y)

plt.axes([0.025,0.025,0.95,0.95]) #设置坐标轴
plt.imshow(Z,interpolation='bicubic', cmap='bone', origin='lower')# 绘制灰度图
plt.colorbar(shrink=.92)# 绘制颜色条

plt.xticks([]), plt.yticks([])
plt.savefig('./imshow_ex.png', dpi=72)# 以分辨率 72 来保存图片
plt.show()
