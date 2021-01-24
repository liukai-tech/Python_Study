# -----------------------------------------------------------------------------
# Copyright (c) 2015, Nicolas P. Rougier. All Rights Reserved.
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------

#!/usr/bin/env python3

#3D 图

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = Axes3D(fig)
X = np.arange(-4, 4, 0.25)
Y = np.arange(-4, 4, 0.25)
X, Y = np.meshgrid(X, Y)
R = np.sqrt(X**2 + Y**2)
Z = np.sin(R)

ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=plt.cm.gist_rainbow) #cmap为调色板，使用plt.cm进行调色
ax.contourf(X, Y, Z, zdir='z', offset=-2, cmap=plt.cm.gist_rainbow)
ax.set_zlim(-2,2)

#plt.savefig('./plot3d_ex.png',dpi=72)
plt.show()
