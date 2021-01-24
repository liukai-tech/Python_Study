#!/usr/bin/python3
 
# 使用qq smtp 发送邮件(发送纯文本格式的内容)

# QQ 邮箱 SMTP 服务器地址：smtp.qq.com，ssl 端口：465。

# 参考网站：https://www.runoob.com/python3/python3-smtp.html https://www.jianshu.com/p/abb2d6e91c1f

import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from email.header import Header
 
my_sender = '792910363@qq.com'    # 发件人邮箱账号
my_pass = 'qfgauhfqpgmubcee'     # 发件人邮箱密码(授权码)
my_receiver = ['liukaitech@gmail.com','792910363@qq.com']  # 收件人邮箱账号，我这边发送给自己(列表类型)

def mail():
    ret = True
    try:
        msg = MIMEText('This is use python3 smtplib send email test(Text Type).', 'plain', 'utf-8')
        msg['From'] = formataddr(["Caesar", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(my_receiver)              # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        subject = 'Python SMTP Email'                       
        msg['Subject'] = Header(subject, 'utf-8')        # 邮件的主题，也可以说是标题
 
        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender, my_receiver, msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        ret = False
    return ret
 
ret = mail()
if ret:
    print("email send success.")
else:
    print("email send failed.")
