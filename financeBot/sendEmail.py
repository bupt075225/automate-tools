#!/usr/bin/env python
# -*- coding:utf-8 -*-

from email import encoders
from email.header import Header
from email.utils import parseaddr, formataddr
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import smtplib

import private

class email(object):
    def __init__(self):
        self.fromAddr = "1335689830@qq.com"
        self.smtpServer = "smtp.qq.com"
        self.password = private.configs['mailAuth']

    def _format_addr(self, s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    def writeEmail(self, **kw):
        msgRoot = MIMEMultipart('related')
        msgRoot['From'] = self._format_addr('助理 <%s>' % self.fromAddr)
        msgRoot['To'] = self._format_addr('老板 <%s>' % kw['toAddr'])
        msgRoot['Subject'] = Header(kw['subject'], 'utf-8').encode()

        # 封装普通文本和HTML两个版本消息体在'alternative'部分,因为
        # 有的邮件代理服务器不支持HTML或客户端设置了只接收普通文本
        msgAlternative = MIMEMultipart('alternative')
        msgRoot.attach(msgAlternative)

        if kw['imageName'] != '':
            with open(kw['imageName'], 'rb') as fp:
                msgImage = MIMEImage(fp.read())

            kw['content'] = kw['content'] + '<br><img src="cid:image1"></br>'
            msgImage.add_header('Content-ID', '<image1>')
            msgRoot.attach(msgImage)

        # 邮件内容是包含一张图片的HTML
        msgText = MIMEText(kw['content'], 'html')
        msgAlternative.attach(msgText)

        return msgRoot

    def sendEmail(self, toAddr, msg):
        server = smtplib.SMTP_SSL(self.smtpServer, 465)
        server.set_debuglevel(1)
        server.login(self.fromAddr, self.password)
        server.sendmail(self.fromAddr, [toAddr], msg.as_string())
        server.quit()
