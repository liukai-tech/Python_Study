#!/usr/bin/python3
 
# 使用qq smtp 发送邮件(发送带附件的邮件)

# 参考网站：https://www.runoob.com/python3/python3-smtp.html https://www.jianshu.com/p/abb2d6e91c1f

import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart
from email.header import Header
 
my_sender = '792910363@qq.com'    # 发件人邮箱账号
my_pass = 'qfgauhfqpgmubcee'     # 发件人邮箱密码(授权码)
my_receiver = ['liukaitech@gmail.com','792910363@qq.com']  # 收件人邮箱账号，我这边发送给自己(列表类型)

def mail():
    ret = True
    try:
        # 创建一个带附件的实例
        msg = MIMEMultipart()
        msg['From'] = formataddr(["Caesar", my_sender])     # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(my_receiver)                 # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        subject = 'Python SMTP Email'                       
        msg['Subject'] = Header(subject, 'utf-8')           # 邮件的主题，也可以说是标题
        
        # 邮件正文内容
        msg.attach(MIMEText('This is Python3 smtp email test(Text Attachments Type).', 'plain', 'utf-8'))
        
        # 构造附件1，传送当前目录下的 test.txt 文件
        #att1 = MIMEText(open('test.txt', 'rb').read(), 'base64', 'utf-8')
        att1 = MIMEText(open('H:/gps nmea data/line.txt', 'rb').read(), 'base64', 'utf-8') # 采用"H:/gps nmea data/line.txt"获取对应目录下文件
        att1["Content-Type"] = 'application/octet-stream'
        # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
        att1["Content-Disposition"] = 'attachment; filename="line.txt"'
        msg.attach(att1)
        
        # 构造附件2，传送当前目录下的 runoob.txt 文件
        #att2 = MIMEText(open('runoob.txt', 'rb').read(), 'base64', 'utf-8')
        att2 = MIMEText(open('H:/gps nmea data/closed circle.txt', 'rb').read(), 'base64', 'utf-8')
        att2["Content-Type"] = 'application/octet-stream'
        att2["Content-Disposition"] = 'attachment; filename="closed circle.txt"'
        msg.attach(att2)
 
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
