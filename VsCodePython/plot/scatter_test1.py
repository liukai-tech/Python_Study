#!/usr/bin/python3

# 极坐标散点图

import numpy as np
import matplotlib.pyplot as plt
import math

N = 10
r = [0.01, 0.0075, 0.0105, 0.0175, 0.0100]

theta = [math.radians(43), math.radians(53), math.radians(67), math.radians(75), math.radians(90)]
colors = 'b'

ax = plt.subplot(111, projection='polar')

c = ax.scatter(theta, r, c=colors, cmap='hsv', alpha=0.75)

plt.show()