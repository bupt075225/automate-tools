#!/usr/bin/env python
# -*- coding:utf-8 -*-

from email import encoders
from email.header import Header
from email.utils import parseaddr, formataddr
from email.mime.text import MIMEText
import smtplib

class email(object):
    def __init__(self):
        self.fromAddr = "1335689830@qq.com"
        self.smtpServer = "smtp.qq.com"
        self.password = ""

    def _format_addr(self, s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    def writeEmail(self, **kw):
        msg = MIMEText(kw['content'], 'plain', 'utf-8')
        msg['From'] = self._format_addr('助理 <%s>' % self.fromAddr)
        msg['To'] = self._format_addr('老板 <%s>' % kw['toAddr'])
        msg['Subject'] = Header(kw['subject'], 'utf-8').encode()
        return msg

    def sendEmail(self, toAddr, msg):
        server = smtplib.SMTP_SSL(self.smtpServer, 465)
        server.set_debuglevel(1)
        server.login(self.fromAddr, self.password)
        server.sendmail(self.fromAddr, [toAddr], msg.as_string())
        server.quit()
