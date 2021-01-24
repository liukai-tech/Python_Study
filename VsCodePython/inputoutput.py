#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

#  repr() 函数可以转义字符串中的特殊字符
hello = 'hello, runoob\n'
print(repr(hello))

# repr() 的参数可以是 Python 的任何对象

# 这里有两种方式输出一个平方与立方的表:
# 方法1
for x in range(1, 11):
    print(repr(x).rjust(2), repr(x*x).rjust(3), end=' ')
    # 注意前一行 'end' 的使用
    print(repr(x*x*x).rjust(4))

# 方法2
for x in range(1, 11):
    print('{0:2d} {1:3d} {2:4d}'.format(x, x*x, x*x*x))

print('\n')


# 打印数字矩阵，使用repr.rjust格式化输出位置
for i in range(1, 11):
    for j in range(1, 11):
        print(repr(i*j).rjust(3), end=' ')
    print('\n')    

'''
注意：在第一个例子中, 每列间的空格由 print() 添加。

这个例子展示了字符串对象的 rjust() 方法, 它可以将字符串靠右, 并在左边填充空格。

还有类似的方法, 如 ljust() 和 center()。 这些方法并不会写任何东西, 它们仅仅返回新的字符串。

另一个方法 zfill(), 它会在数字的左边填充 0，如下所示：
'''

stra = '12'
print(stra.zfill(5))

strb = '-3.1415'
print(strb.zfill(10))

# str.format() 的基本使用如下:
print('{}网址： "{}!"'.format('菜鸟教程', 'www.runoob.com'))

# 括号及其里面的字符 (称作格式化字段) 将会被 format() 中的参数替换。
# 在括号中的数字用于指向传入对象在 format() 中的位置，如下所示：
print('{0} 和 {1}'.format('Google', 'Runoob'))
print('{1} 和 {0}'.format('Google', 'Runoob'))

# 如果在 format() 中使用了关键字参数, 那么它们的值会指向使用该名字的参数。
print('{name}网址： {site}'.format(name='菜鸟教程', site='www.runoob.com'))

# 位置及关键字参数可以任意的结合:
print('站点列表 {0}, {1}, 和 {other}。'.format('Google', 'Runoob', other='Taobao'))

# !a (使用 ascii()), !s (使用 str()) 和 !r (使用 repr()) 可以用于在格式化某个值之前对其进行转化:
import math
print('常量 PI 的值近似为： {}。'.format(math.pi))
print('常量 PI 的值近似为： {!r}。'.format(math.pi))

# 可选项 : 和格式标识符可以跟着字段名。 这就允许对值进行更好的格式化。 下面的例子将 Pi 保留到小数点后三位：
print('常量 PI 的值近似为: {0:.5f}。'.format(math.pi))

# 在 : 后传入一个整数, 可以保证该域至少有这么多的宽度。 用于美化表格时很有用。
table = {'Google': 1, 'Runoob': 2, 'Taobao': 3}
for name, number in table.items():
    print('{0:10} ==> {1:10d}'.format(name, number))



