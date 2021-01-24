# -----------------------------------------------------------------------------
# Copyright (c) 2015, Nicolas P. Rougier. All Rights Reserved.
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------

#!/usr/bin/env python3

#条形图

import numpy as np
import matplotlib.pyplot as plt

n = 12
X = np.arange(n)
Y1 = (1-X/float(n)) * np.random.uniform(0.5,1.0,n) #随机生成条形码数值array
Y2 = (1-X/float(n)) * np.random.uniform(0.5,1.0,n)

print('X:',X,'type:',type(X))
print('Y1:',Y1,'type:',type(Y1))

plt.axes([0.025,0.025,0.95,0.95]) #设置坐标轴
plt.bar(X, +Y1, facecolor='#9999ff', edgecolor='white') #绘制条形码
plt.bar(X, -Y2, facecolor='#ff9999', edgecolor='white')

for x,y in zip(X,Y1):
    plt.text(x, y+0.05, '%.2f' % y, ha='center', va= 'bottom') #在对应条形码下方放置条形码数值

for x,y in zip(X,Y2):
    plt.text(x, -y-0.05, '%.2f' % y, ha='center', va= 'top') #在对应条形码上方放置条形码数值

# 设置横纵坐标上下限及记号
plt.xlim(-.5,n), plt.xticks([])
plt.ylim(-1.25,+1.25), plt.yticks([])

#plt.savefig('./bar_ex.png', dpi=72) )# 以分辨率 72 来保存图片
plt.show()
