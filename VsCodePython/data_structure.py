#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

a = [66.25, 333, 333, 1, 1234.5]
print(a.count(333), a.count(66.25), a.count('x'))

a.insert(2, -1)
a.append(333)
print(a)

# 将列表当做堆栈使用（后入先出）
stack = [3, 4, 5]

stack.append(6)
stack.append(7)
print(stack)

stack.pop()
print(stack)
stack.pop()
print(stack)

# 将列表当作队列使用(FIFO)
from collections import deque

queue = deque(["Eric", "John", "Michael"])
queue.append("Terry")  # Terry arrives
queue.append("Graham")  # Graham arrives
print(queue)
queue.popleft()  # The first to arrive now leaves
print(queue)
queue.popleft()  # The second to arrive now leaves
print(queue)

# 列表推导式
vec = [2, 4, 6]
print([3 * x for x in vec])

print([[x, x**2] for x in vec])

# 可以用 if 子句作为过滤器
print([3 * x for x in vec if x > 3])

vec1 = [2, 4, 6]
vec2 = [4, 3, -9]
print([x * y for x in vec1 for y in vec2])
print([x + y for x in vec1 for y in vec2])
print([vec1[i] * vec2[i] for i in range(len(vec1))])

# 列表推导式可以使用复杂表达式或嵌套函数
print([str(round(355 / 113, i)) for i in range(1, 6)])

# 3*4矩阵
matrix = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
]

# 方法1，将3*4矩阵变换为4*3矩阵[[1, 5, 9], [2, 6, 10], [3, 7, 11], [4, 8, 12]]
print([[row[i] for row in matrix] for i in range(len(matrix))])
'''
矩阵变换执行顺序是：
for i in range(len(matrix))
    for row in matrix
        row[i]
'''

# 方法2
transposed = []
for i in range(len(matrix)):
    transposed.append([row[i] for row in matrix])

print(transposed)

# 方法3
transposed2 = []
for i in range(len(matrix)):
    transposed_row = []
    for row in matrix:
        transposed_row.append(row[i])
    transposed2.append(transposed_row)

print(transposed2)

# 集合
a = set('abracadabra')
print(a)

# 集合也支持推导式
a1 = {x for x in 'abracadabra' if x not in 'abc'}
print(a1)

# 字典
tel = {'jack': 4098, 'sape': 4139}
tel['Caesar'] = 4090
print(tel)
print(list(tel.keys()))
print(list(tel.values()))

# 构造字典
print(dict([('sape', 4139), ('guido', 4127), ('jack', 4098)]))
print(dict(sape=4139, guido=4127, jack=4098))

# 推导式
print({x: x**2 for x in (2, 4, 6)})

# 遍历技巧
knights = {'gallahad': 'the pure', 'robin': 'the brave'}
for k, v in knights.items():
    print('key:', k, 'value:', v)

# 在序列中遍历时，索引位置和对应值可以使用 enumerate() 函数同时得到
for i, v in enumerate(['tic', 'tac', 'toe']):
    print('i:', i, 'v:', v)

# 同时遍历两个或更多的序列，可以使用 zip() 组合
questions = ['name', 'quest', 'favorite color']
answers = ['lancelot', 'the holy grail', 'blue']
for q, a in zip(questions, answers):
    print('questions:', q, 'answers:', a)

# 要反向遍历一个序列，首先指定这个序列，然后调用 reversed() 函数
for i in reversed(range(1, 10, 1)):
    print(i)

# 要按顺序遍历一个序列，使用 sorted() 函数返回一个已排序的序列，并不修改原值
basket = ['apple', 'orange', 'apple', 'pear', 'orange', 'banana']
for i in sorted(set(basket)):
    print(i)
'''
列表推导式（又称列表解析式）提供了一种简明扼要的方法来创建列表。

它的结构是在一个中括号里包含一个表达式，然后是一个for语句，然后是 0 个或多个 for 或者 if 语句。那个表达式可以是任意的，意思是你可以在列表中放入任意类型的对象。返回结果将是一个新的列表，在这个以 if 和 for 语句为上下文的表达式运行完成之后产生。

列表推导式的执行顺序：各语句之间是嵌套关系，左边第二个语句是最外层，依次往右进一层，左边第一条语句是最后一层。

[x*y for x in range(1,5) if x > 2 for y in range(1,4) if y < 3]

执行顺序是：
for x in range(1,5)
    if x > 2
        for y in range(1,4)
            if y < 3
                x*y

'''
# 有多个列表需要遍历时，需要zip，除了用'{0}{1}'.format(q,a)的方法，还可以使用%s方法（两者效果一样一样的）：

questions = ['name', 'quest', 'favorite color']
answers = ['qinshihuang', 'the holy', 'blue']
for q, a in zip(questions, answers):
    print('what is your %s? it is %s' % (q, a))
    print('what is your {0}? it is {1}'.format(q, a))

# pynmea2 module parse test
import pynmea2

gga = '$GPGGA,072034.00,3905.8186042,N,11704.9435945,E,4,18,0.8,1.6436,M,-8.922,M,01,0004*4B'
ggainfo = pynmea2.parse(gga, True)
print('pynmea2 version:', pynmea2.version)
print('parse ggainfo:', repr(ggainfo))
