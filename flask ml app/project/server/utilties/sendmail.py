import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

from project.server import app


def send_mail(fromEmail, password, toEmail, subject, body):

    msg = MIMEMultipart()
    msg['From'] = fromEmail
    msg['To'] = toEmail
    msg['Subject'] = subject
    body = MIMEText(body, 'html', 'utf-8')
    msg.attach(body)

    file_path = "D:\\TestFile"
    if file_path is not None:
        for childfile in os.listdir(file_path):
            childFilePath = os.path.join(file_path,childfile)
            if not os.path.isdir(childFilePath):
                p = MIMEBase('application', "octet-stream")
                p.set_payload(open(childFilePath, "rb").read())
                encoders.encode_base64(p)
                p.add_header('Content-Disposition', 'attachment' ,filename=childfile)
                msg.attach(p)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromEmail, password)
    text = msg.as_string()
    s.sendmail(fromEmail, toEmail, text)
    s.quit()

def send_notification(toEmail, subject, body):
    fromEmail = app.config["serviceEmail"]
    password = app.config["password"]
    send_mail(fromEmail, password, toEmail, subject, body)
