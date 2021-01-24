#!/usr/bin/python3

#9*9乘法法则

#外边一层循环控制行数

i = 1
while i <= 9:
    j = 1
    while j <= i:
        muti = j * i
        print("%d*%d=%d" % (j, i, muti), end = "  ")
        j += 1
    print("")
    i += 1
    
