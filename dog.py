#!/usr/bin/python3 
 
# 该实例演示了狗狗年龄对比系统

'''

print("=======欢迎进入狗狗年龄对比系统========")
while True:
    try:
        age = int(input("请输入您家狗的年龄:"))
        print(" ")
        age = float(age)
        if age < 0:
            print("您在逗我？")
        elif age == 1:
            print("相当于人类14岁")
            break
        elif age == 2:
            print("相当于人类22岁")
            break
        else:
            human = 22 + (age - 2)*5
            print("相当于人类：",human)
            break
    except ValueError:
        print("输入不合法，请输入有效年龄")
###退出提示
input("点击 enter 键退出")

'''

# 继续扩展，加入用户提示判断是否退出还是继续

print("=======欢迎进入狗狗年龄对比系统========")
control = "N"
while control=="N":
    try:
        age = int(input("请输入您家狗的年龄:"))
        #print(" ")
        age = float(age)
        if age < 0:
            print("您在逗我？")
        elif age == 1:
            print("相当于人类14岁")
            #break
        elif age == 2:
            print("相当于人类22岁")
            #break
        else:
            human = 22 + (age - 2)*5
            print("相当于人类：",human)
            #break
    except ValueError:
        print("输入不合法，请输入有效年龄")
    print("")
    control = input("退出(Y/N)？")
    print("")
###退出提示
input("点击 enter 键退出")
