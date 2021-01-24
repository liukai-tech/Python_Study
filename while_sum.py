#!/usr/bin/env python3

#以下实例使用了 while 来计算 1 到 100 的总和
 
n = 100
 
sum = 0
counter = 1
while counter <= n:
    sum = sum + counter
    counter += 1
 
print("1 到 %d 之和为: %d" % (n,sum))
