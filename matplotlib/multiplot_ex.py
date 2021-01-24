# -----------------------------------------------------------------------------
# Copyright (c) 2015, Nicolas P. Rougier. All Rights Reserved.
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------

#!/usr/bin/env python3

#多重网格图

import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure()
#fig.subplots_adjust(bottom=0.025, left=0.025, top = 0.975, right=0.975)

plt.subplot(2,1,1)
plt.xticks([]), plt.yticks([])

plt.subplot(2,3,4) #此处index=4，需要跳过2,3编号
plt.xticks([]), plt.yticks([])

plt.subplot(2,3,5)
plt.xticks([]), plt.yticks([])

plt.subplot(2,3,6)
plt.xticks([]), plt.yticks([])
#plt.subplot(2,3,6,projection='polar') #绘制雷达图

#plt.savefig('./multiplot_ex.png',dpi=72)
plt.show()
