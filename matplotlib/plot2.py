#!/usr/bin/env python3

# 导入 matplotlib.pyplot及numpy模块
import numpy as np
import matplotlib.pyplot as plt


n = 256
X = np.linspace(-np.pi, np.pi, n, endpoint=True)
Y = np.sin(2*X)

plt.plot(X, Y+1, color='blue', alpha=1.00)
plt.plot(X, Y-1, color='blue', alpha=1.00)

plt.show()

