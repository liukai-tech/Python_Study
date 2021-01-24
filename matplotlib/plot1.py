#!/usr/bin/env python3

# 导入 matplotlib.pyplot及numpy模块
import numpy as np
import matplotlib.pyplot as plt

# 创建一个 10 * 6 点（point）的图，并设置分辨率为 80
plt.figure(figsize=(10,6), dpi=80)


# 创建一个新的 1 * 1 的子图，接下来的图样绘制在其中的第 1 块（也是唯一的一块）
plt.subplot(1,1,1)


X = np.linspace(-np.pi, np.pi, 256, endpoint=True)
C,S = np.cos(X), np.sin(X)

# 绘制余弦曲线，使用蓝色的、连续的、宽度为 2.5 （像素）的线条
plt.plot(X, C, color="blue", linewidth=2.5, linestyle="-", label="cosine")

# 绘制正弦曲线，使用红色的、连续的、宽度为 2.5 （像素）的线条
plt.plot(X, S, color="red",  linewidth=2.5, linestyle="-", label="sine")

# 设置横纵轴的上下限
xmin ,xmax = X.min(), X.max()
ymin, ymax = C.min(), C.max()

dx = (xmax - xmin) * 0.2
dy = (ymax - ymin) * 0.2

plt.xlim(xmin - dx, xmax + dx)
plt.ylim(ymin - dy, ymax + dy)

# 设置横纵轴记号

plt.xticks([-np.pi, -np.pi/2, 0, np.pi/2, np.pi],
       [r'$-\pi$', r'$-\pi/2$', r'$0$', r'$+\pi/2$', r'$+\pi$'])

plt.yticks([-1, 0, +1],
       [r'$-1$', r'$0$', r'$+1$'])

# 移动脊柱
ax = plt.gca()
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.spines['bottom'].set_position(('data',0))
ax.yaxis.set_ticks_position('left')
ax.spines['left'].set_position(('data',0))

# 精益求精
for label in ax.get_xticklabels() + ax.get_yticklabels():
    label.set_fontsize(16)
    label.set_bbox(dict(facecolor='white', edgecolor='None', alpha=0.65 ))

# 设置网格
#plt.grid()

# 添加图例
plt.legend(loc='upper left')

# 给一些特殊点做注释
'''
我们希望在 2π/3 的位置给两条函数曲线加上一个注释。首先，我们在对应的函
数图像位置上画一个点；然后，向横轴引一条垂线，以虚线标记；最后，写上标签。
'''

t = 2*np.pi/3
plt.plot([t,t],[0,np.cos(t)], color ='blue', linewidth=2.5, linestyle="--")
plt.scatter([t,],[np.cos(t),], 50, color ='blue')

plt.annotate(r'$\sin(\frac{2\pi}{3})=\frac{\sqrt{3}}{2}$',
         xy=(t, np.sin(t)), xycoords='data',
         xytext=(+10, +30), textcoords='offset points', fontsize=16,
         arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))

plt.plot([t,t],[0,np.sin(t)], color ='red', linewidth=2.5, linestyle="--")
plt.scatter([t,],[np.sin(t),], 50, color ='red')

plt.annotate(r'$\cos(\frac{2\pi}{3})=-\frac{1}{2}$',
         xy=(t, np.cos(t)), xycoords='data',
         xytext=(-90, -50), textcoords='offset points', fontsize=16,
         arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))



# 以分辨率 72 来保存图片
#plt.savefig("./plot1.png",dpi=72)

# 在屏幕上显示
plt.show()
