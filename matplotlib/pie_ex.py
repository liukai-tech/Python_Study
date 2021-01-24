# -----------------------------------------------------------------------------
# Copyright (c) 2015, Nicolas P. Rougier. All Rights Reserved.
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------

#!/usr/bin/env python3

#饼状图

import numpy as np
import matplotlib.pyplot as plt

n = 20
Z = np.ones(n)
Z[-1] *= 2 # 生成最后一个数据等于2的np array

#print('Z',Z, 'type',type(Z))

plt.axes([0.025, 0.025, 0.95, 0.95])

#plt.pie(Z) #直接绘制饼状图

plt.pie(Z, explode=Z*.05, colors=['%f' % (i/float(n)) for i in range(n)],
        wedgeprops={"linewidth": 1, "edgecolor": "black"})
plt.gca().set_aspect('equal')
plt.xticks([]), plt.yticks([])

#plt.savefig('./pie_ex.png',dpi=72)
plt.show()
