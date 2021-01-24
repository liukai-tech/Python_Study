# -----------------------------------------------------------------------------
# Copyright (c) 2015, Nicolas P. Rougier. All Rights Reserved.
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------

#!/usr/bin/env python3

#散点图


import numpy as np
import matplotlib.pyplot as plt

n = 1024
X = np.random.normal(0,1,n) # XY轴生成0-1随机点集
Y = np.random.normal(0,1,n)
T = np.arctan2(Y,X)

plt.axes([0.025,0.025,0.95,0.95]) # 设置坐标轴
plt.scatter(X,Y, s=75, c=T, alpha=.5)  # 绘制散点图，s控制散点圆大小,c为颜色的序列

# 设置横纵坐标上下限及记号
plt.xlim(-1.5,1.5), plt.xticks([])
plt.ylim(-1.5,1.5), plt.yticks([])
#plt.savefig('./scatter_ex.png',dpi=72)
plt.show()
