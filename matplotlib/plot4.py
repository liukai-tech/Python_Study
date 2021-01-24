import numpy as np
import matplotlib.pyplot as plt

def f(x, y):
    return (1-x/2+x**5+y**3) * np.exp(-x**2-y**2)

n = 256
x = np.linspace(-3, 3, n)
y = np.linspace(-3, 3, n)
X,Y = np.meshgrid(x, y)

plt.contourf(X, Y, f(X, Y), 8, alpha=.75, cmap='jet')
C = plt.contour(X, Y, f(X, Y), 8, colors='black', linewidths=.5)

# 设置横纵坐标上下限及记号
plt.xlim(-3,3), plt.xticks([])
plt.ylim(-3,3), plt.yticks([])

plt.show()
