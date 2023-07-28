from smtplib import SMTP_SSL
from email.mime.text import MIMEText


def sendMail(message, Subject, sender_show, recipient_show, to_addrs, cc_show=''):

    # 填写真实的发邮件服务器用户名、密码
    user = 'xiaobaibaiyang@163.com'
    password = 'SCHMSLSYVYKWYPPV'
    # 邮件内容
    msg = MIMEText(message, 'html', _charset="utf-8")
    # 邮件主题描述
    msg["Subject"] = Subject
    # 发件人显示，不起实际作用
    msg["from"] = sender_show
    # 收件人显示，不起实际作用
    msg["to"] = recipient_show
    # 抄送人显示，不起实际作用
    msg["Cc"] = cc_show
    with SMTP_SSL(host="smtp.163.com", port=465) as smtp:
        # 登录发邮件服务器
        smtp.login(user=user, password=password)
        # 实际发送、接收邮件配置
        smtp.sendmail(from_addr=user, to_addrs=to_addrs.split(','), msg=msg.as_string())



