import smtplib
import email
# 负责构造文本
from email.mime.text import MIMEText
# 负责构造图片
from email.mime.image import MIMEImage
# 负责将多个对象集合起来
from email.mime.multipart import MIMEMultipart
from email.header import Header
import sys
sys.path.append('.//')
from utils import csv_to_html

# SMTP服务器,这里使用163邮箱
mail_host = "smtp.qq.com"
# 发件人邮箱
mail_sender = "596908514@qq.com"
# 邮箱授权码,注意这里不是邮箱密码,如何获取邮箱授权码,请看本文最后教程
mail_license = "kgtfmommembqbfai"
# 收件人邮箱，可以为多个收件人
mail_receivers = ["596908514@qq.com", "919736062@qq.com"]

mm = MIMEMultipart('alternative')

# 邮件主题
subject_content = "No appointment found!"
# 设置发送者,注意严格遵守格式,里面邮箱为发件人邮箱
mm["From"] = mail_sender
# 设置邮件主题
mm["Subject"] = Header(subject_content)

# 邮件正文内容
body_content = "1"
# 构造文本,参数1：正文内容，参数2：文本格式，参数3：编码方式
message_text = MIMEText(body_content,"plain", 'utf-8')
# 向MIMEMultipart对象中添加文本对象
mm.attach(message_text)

mail_body = open(csv_to_html(), 'r').read()

message_html = MIMEText(mail_body, 'html', 'utf-8')
mm.attach(message_html)

# 创建SMTP对象
stp = smtplib.SMTP()
# 设置发件人邮箱的域名和端口，端口地址为465
stp.connect(mail_host, 587)  
# set_debuglevel(1)可以打印出和SMTP服务器交互的所有信息
stp.set_debuglevel(1)
# 登录邮箱，传递参数1：邮箱地址，参数2：邮箱授权码
stp.login(mail_sender,mail_license)
print('登录成功')
# 发送邮件，传递参数1：发件人邮箱地址，参数2：收件人邮箱地址，参数3：把邮件内容格式改为str
stp.sendmail(mail_sender, mail_receivers, mm.as_string())
print("邮件发送成功")
# 关闭SMTP对象
stp.quit()