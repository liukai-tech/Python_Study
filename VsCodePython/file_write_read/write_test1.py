#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
不同模式打开文件的完全列表：

r	以只读方式打开文件。文件的指针将会放在文件的开头。这是默认模式。
rb	以二进制格式打开一个文件用于只读。文件指针将会放在文件的开头。
r+	打开一个文件用于读写。文件指针将会放在文件的开头。
rb+	以二进制格式打开一个文件用于读写。文件指针将会放在文件的开头。
w	打开一个文件只用于写入。如果该文件已存在则打开文件，并从开头开始编辑，即原有内容会被删除。如果该文件不存在，创建新文件。
wb	以二进制格式打开一个文件只用于写入。如果该文件已存在则打开文件，并从开头开始编辑，即原有内容会被删除。如果该文件不存在，创建新文件。
w+	打开一个文件用于读写。如果该文件已存在则打开文件，并从开头开始编辑，即原有内容会被删除。如果该文件不存在，创建新文件。
wb+	以二进制格式打开一个文件用于读写。如果该文件已存在则打开文件，并从开头开始编辑，即原有内容会被删除。如果该文件不存在，创建新文件。
a	打开一个文件用于追加。如果该文件已存在，文件指针将会放在文件的结尾。也就是说，新的内容将会被写入到已有内容之后。如果该文件不存在，创建新文件进行写入。
ab	以二进制格式打开一个文件用于追加。如果该文件已存在，文件指针将会放在文件的结尾。也就是说，新的内容将会被写入到已有内容之后。如果该文件不存在，创建新文件进行写入。
a+	打开一个文件用于读写。如果该文件已存在，文件指针将会放在文件的结尾。文件打开时会是追加模式。如果该文件不存在，创建新文件用于读写。
ab+	以二进制格式打开一个文件用于追加。如果该文件已存在，文件指针将会放在文件的结尾。如果该文件不存在，创建新文件用于读写。

模式	    r	r+	w	w+	a	a+
读	        +	+		+		+
写		        +	+	+	+	+
创建			    +	+	+	+
覆盖			    +	+		
指针在开始	+	+	+	+		
指针在结尾					+	+

'''

# 1.以覆盖写入的方式打开一个文件
print('1.Warp Write to file')
f = open("H:/python study/VsCodePython/file_write_read/write_test1.txt", "w")

num = f.write("Python 是一个非常好的语言。\n是的，的确非常好!!\n")
print('write data size:', num)

# 关闭打开的文件
f.close()

# 2.以读的方式打开一个文件
print('\n2.Open Read-Only file,read all text')
f = open("H:/python study/VsCodePython/file_write_read/write_test1.txt", "r")

# 读取文件内所有内容，size可选
rdstr = f.read()
print(rdstr)

# 关闭打开的文件
f.close()

# 3.以读的方式打开一个文件
print('\n3.Open Read-Only file,read one line')
f = open("H:/python study/VsCodePython/file_write_read/write_test1.txt", "r")

# f.readline() 会从文件中读取单独的一行。换行符为 '\n'。f.readline() 如果返回一个空字符串, 说明已经已经读取到最后一行。
rdstr = f.readline()
print(rdstr)

# 关闭打开的文件
f.close()

# 4.以读的方式打开一个文件
print('\n4.Open Read-Only file,read all lines split by \\n')
f = open("H:/python study/VsCodePython/file_write_read/write_test1.txt", "r")

# f.readlines() 将返回该文件中包含的所有行。
# 如果设置可选参数 sizehint, 则读取指定长度的字节, 并且将这些字节按行分割。
rdstr = f.readlines()
print(rdstr)

# 关闭打开的文件
f.close()

# 5.以读的方式打开一个文件
print('\n5.Open Read-Only file,read line iteration')
f = open("H:/python study/VsCodePython/file_write_read/write_test1.txt", "r")

for line in f:
    print(line, end='')

# 关闭打开的文件
f.close()

# 如果要写入一些不是字符串的东西, 那么将需要先进行转换

# 打开一个文件
print('\n6.Wrap Write to file,special type obj need convert to string')
f = open("H:/python study/VsCodePython/file_write_read/write_test1-2.txt", "w")

value = ('www.google.com', 14)  # tuple
value_str = str(value)
f.write(value_str)

# 关闭打开的文件
f.close()

# 当处理一个文件对象时, 使用 with 关键字是非常好的方式。在结束后, 它会帮你正确的关闭文件。 而且写起来也比 try - finally 语句块要简短:

with open('H:/python study/VsCodePython/file_write_read/write_test1.txt', 'r') as f:
    read_data = f.read()

print(read_data, 'file closed:', f.closed)

