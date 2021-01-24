#!/usr/bin/python3
 
# 使用qq smtp 发送邮件(在 HTML 文本中添加图片)

# 参考网站：https://www.runoob.com/python3/python3-smtp.html https://www.jianshu.com/p/abb2d6e91c1f


import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
 
my_sender = '792910363@qq.com'    # 发件人邮箱账号
my_pass = 'qfgauhfqpgmubcee'     # 发件人邮箱密码(授权码)
my_receiver = ['liukaitech@gmail.com','792910363@qq.com']  # 收件人邮箱账号，我这边发送给自己(列表类型)

def mail():
    ret = True
    try:
        msgRoot = MIMEMultipart('related')
        msgRoot['From'] = formataddr(["Caesar", my_sender])     # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msgRoot['To'] = formataddr(my_receiver)                 # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        subject = 'Python SMTP Email'
        msgRoot['Subject'] = Header(subject, 'utf-8')           # 邮件的主题，也可以说是标题
        
        msgAlternative = MIMEMultipart('alternative')
        msgRoot.attach(msgAlternative)
                
        mail_msg = """
<p>This is Python3 smtp email test(HTML + Picture Type).</p>
<p><a href="https://github.com/Knio/pynmea2">This is pynmea2 github link url</a></p>
<p>Picture Show：</p>
<p><img src="cid:image1"></p>
"""
        msgAlternative.attach(MIMEText(mail_msg, 'html', 'utf-8'))
        
        
        #fp = open('test.png', 'rb')    # 指定图片为当前目录
        fp = open('H:/tmp/pic/Python1.png', 'rb')   # 打开指定目录下的图片文件
        msgImage = MIMEImage(fp.read())
        fp.close()
        
        # 定义图片 ID，在 HTML 文本中引用
        msgImage.add_header('Content-ID', '<image1>')
        msgRoot.attach(msgImage)
 
        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender, my_receiver, msgRoot.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号(列表类型)、发送邮件
        server.quit()  # 关闭连接
    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        ret = False
    return ret
 
ret = mail()
if ret:
    print("email send success.")
else:
    print("email send failed.")
