# -----------------------------------------------------------------------------
# Copyright (c) 2015, Nicolas P. Rougier. All Rights Reserved.
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------

#!/usr/bin/env python3

#普通图，填充

import numpy as np
import matplotlib.pyplot as plt

n = 256
X = np.linspace(-np.pi,np.pi,n,endpoint=True) #生成X轴数据
Y = np.sin(2*X) #生成Y轴数据 

plt.axes([0.025,0.025,0.95,0.95]) #设置坐标轴

plt.plot (X, Y+1, color='blue', alpha=1.00) #绘制曲线
plt.fill_between(X, 1, Y+1, color='blue', alpha=.25) #填充1至Y+1两条曲线之间的区域

plt.plot (X, Y-1, color='blue', alpha=1.00) #绘制另一条曲线
plt.fill_between(X, -1, Y-1, (Y-1) > -1, color='blue', alpha=.25) 
plt.fill_between(X, -1, Y-1, (Y-1) < -1, color='red',  alpha=.25)

# 设置横纵坐标上下限及记号
plt.xlim(-np.pi,np.pi), plt.xticks([])
plt.ylim(-2.5,2.5), plt.yticks([])
plt.savefig('./plot_ex.png',dpi=72)# 以分辨率 72 来保存图片
plt.show()
