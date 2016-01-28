#! /usr/local/bin/python
import sys
import os

from smtplib import SMTP_SSL as SMTP       # this invokes the secure SMTP protocol (port 465, uses SSL)
# from smtplib import SMTP                  # use this for standard SMTP protocol   (port 25, no encryption)
from email.MIMEText import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from os.path import basename
import json

directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
email_config_file = os.path.join(directory, "email.config")
email_config = json.loads(open(email_config_file, "rb").read())

SMTPserver = email_config["smtp_sever"]
sender = email_config["sender"]
destination = email_config["destination"]

USERNAME = email_config["username"]
PASSWORD = email_config["password"]

text_subtype = 'plain'

content="""\
Check attached csv report.
"""

subject="Sent from news crawler - vip news updates!"

def send_email(report_file):
    try:
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = sender # some SMTP servers will do this automatically, not all
        msg.attach(MIMEText(content))

        with open(report_file, 'rb') as fil:
            msg.attach(MIMEApplication(
                fil.read(),
                Content_Disposition='attachment; filename="%s"' % basename(report_file),
                Name=basename(report_file)
            ))
        
        conn = SMTP(SMTPserver)
        conn.set_debuglevel(False)
        conn.login(USERNAME, PASSWORD)
        
        try:
            conn.sendmail(sender, destination, msg.as_string())
        finally:
            conn.close()
    
    except Exception, exc:
        #log message
        print "UNABLE to send email..check internet connection please..."
        pass
        
def test_send_email():
    directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    email_report_file = os.path.join(directory, "reports.csv")
    send_email(email_report_file)
    
# test_send_email()