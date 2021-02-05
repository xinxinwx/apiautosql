import datetime
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText  # 传附件


class SendEmail:
    global send_user
    global email_host
    global password
    email_host = "smtp.qq.com"
    send_user = "380222985@qq.com"
    password = "eyteexarlvghbhhg"
    # send_user = ''
    # password = ''

    def send_main(self, pass_list, fail_list):
        # 邮件发送给谁
        user_list = ['776787883@qq.com']

        user = "测试报告" + "<" + send_user + ">"
        message = MIMEMultipart()
        message['From'] = user
        message['To'] = ";".join(user_list)
        pass_num = float(len(pass_list))
        fail_num = float(len(fail_list))
        count_num = pass_num+fail_num
        # 取小数点后两位
        pass_result = "%.2f%%" % (pass_num/count_num*100)
        fail_result = "%.2f%%" % (fail_num/count_num*100)
        content = "此次一共运行接口个数为{}个,通过个数为{}个,失败个数为{},通过率为{},失败率为{}".format(count_num, pass_num, fail_num, pass_result, fail_result)
        sub = content
        message['Subject'] = sub

        filename = '../log/log.txt'
        time = datetime.date.today()
        att = MIMEText(open(filename, 'rb').read(), 'base64', 'utf-8')
        att["Content-Type"] = 'application/octet-stream'
        att["Content-Disposition"] = 'attachment; filename="%s_Log.txt"' % time
        message.attach(att)

        apifilename = '../log/api.txt'
        time = datetime.date.today()
        att = MIMEText(open(apifilename, 'rb').read(), 'base64', 'utf-8')
        att["Content-Type"] = 'application/octet-stream'
        att["Content-Disposition"] = 'attachment; filename="%s_Api.txt"' % time
        message.attach(att)

        # windows发送邮件
        server = smtplib.SMTP()
        server.connect(email_host)
        # linux发送邮件
        # server = smtplib.SMTP_SSL(email_host, 465)

        server.login(send_user, password)
        server.sendmail(send_user, user_list, message.as_string())
        server.close()


if __name__ == '__main__':
    sen = SendEmail()
    sen.send_main([], [1, 2, 3])
