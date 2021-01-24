#!/usr/bin/env python3


# 取随机数直到两数相等，显示取数次数及消耗时间

import random
import time

rangemax = 1000
a = 0
start = time.time()
while True:    
    x = random.choice(range(rangemax))
    y = random.choice(range(rangemax))
    a += 1    
    if x > y:        
        print(x,'>',y)
    elif x < y:        
        print(x,'<',y)
    else:        
        print('x=y=', x, 'total cal ', a, 'times')
        end = time.time()
        print("运行时间:%.2f秒"%(end-start))
        break
