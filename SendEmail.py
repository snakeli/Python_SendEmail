##################################
# Author: Junjun.Li
# Script Description: For OS Performance test report auto sending.
# Precondition: You should put email_credentials.cfg to your script folder.
####################################

# !/usr/bin/python
# -*-coding:utf-8-*-

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart, MIMEBase
from email.utils import parseaddr, formataddr
import smtplib
import os

CONFIG = {'FROM': r'', 'PASSWORD': r'', 'TO': [], 'SMTP': r''}


def _format_add(address):
    name, addr = parseaddr(address)
    return formataddr((Header(name, 'utf-8').encode(),
                       addr.encode('utf-8') if isinstance(addr, unicode) else addr))


# Read mail_credentials file to get the Email account and credential details
def read_config_file():
    home_dir = os.path.split(os.path.realpath(__file__))[0] + "/"
    print "home_dir: " + home_dir
    if "HOME" in os.environ:
        doc_root = os.environ["HOME"]
        home_dir = doc_root + "/"
    filename_with_path = home_dir + 'email_credentials.cfg'

    try:
        fin = open(filename_with_path, 'r')
        for line in fin:
            (key, value) = line.rstrip().split('=')
            if key == "TO":
                CONFIG['TO'].append(value)
            else:
                CONFIG[key.strip()] = value.strip()
        fin.close()
    except Exception, e:
        print 'read_config_file - error while opening file: %s' % filename_with_path
        print e


def send_mail():
    from_addr = CONFIG['FROM']
    password = CONFIG['PASSWORD']
    smtp_server = CONFIG['SMTP']
    to_addr = CONFIG['TO']

    # Email object
    msg = MIMEMultipart()
    msg['From'] = _format_add(u"OSPerformance<%s>" % from_addr)
    msg['To'] = _format_add(u"Tester<%s>" % to_addr)
    msg['Subject'] = Header(u"OSPerformance test finish...", "utf-8").encode()
    # Email body
    msg.attach(MIMEText('Test finished. \nResult please refer to the attachment'))
    # Email attachment
    with open('E:/Automation/performance_1117/performance/Binaries/ProfileTargets/AOStargets/square-compat.xml', 'rb') as f:
        mime = MIMEBase('xml', 'xml', filename='test.xml')
        mime.add_header('Content-Disposition', 'attachment', filename='test.xml')
        mime.add_header('Content-ID', '<0>')
        mime.add_header('X-Attachment-ID', '0')
        mime.set_payload(f.read())
        encoders.encode_base64(mime)
        msg.attach(mime)

    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()

if __name__ == '__main__':
    read_config_file()
    send_mail()
