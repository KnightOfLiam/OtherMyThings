import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email():
    # 配置参数
    smtp_server = "mail.deathknight.work.gd"
    smtp_port = 587
    username = "admin@mail.deathknight.work.gd"
    password = "123456"  # 替换为实际密码

    # 创建邮件对象
    msg = MIMEMultipart()
    msg["From"] = username
    # msg["To"] = "test-ay3ud5cp3@srv1.mail-tester.com"  # 收件人邮箱
    msg["To"] = "a61628904@163.com"  # 收件人邮箱
    msg["Subject"] = "Python自动化测试邮件"

    # 添加邮件正文
    body = "这是一封通过Python自动发送的测试邮件"
    msg.attach(MIMEText(body, "plain"))

    # 发送邮件
    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(username, password)

            server.sendmail(username, msg["To"], msg.as_string())
        print("邮件发送成功！")
    except Exception as e:
        print(f"发送失败: {str(e)}")

# 执行发送
send_email()
