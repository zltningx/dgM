# -*- coding: utf-8 -*-
# author: zltningx

import smtplib

from email.header import Header
from email.mime.text import MIMEText
from email.utils import formataddr, parseaddr
from typing import List
from django.core.validators import EmailValidator


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def send_dragon_m_email(
        smtp_host: str,
        smtp_port: int,
        smtp_username: str,
        smtp_password: str,
        smtp_encryption: str,
        from_addr: str,
        to_addrs: List[str],
        subject: str,
        content: str,
):
    if not all([EmailValidator(i) for i in to_addrs]):
        raise Exception("接收邮件列表验证不通过")
    if not EmailValidator(from_addr):
        raise Exception("发送邮件验证不通过")

    email = MIMEText(content, 'html', 'utf-8')
    email['From'] = _format_addr(f'DragonM 安全平台 <{from_addr}>')
    email['To'] = ','.join([_format_addr(i) for i in to_addrs])
    email['Subject'] = Header(subject, 'utf-8').encode()

    if smtp_encryption == "NONE":
        worker = smtplib.SMTP(smtp_host, smtp_port)
    elif smtp_encryption == "SSL":
        worker = smtplib.SMTP_SSL(smtp_host, smtp_port)
    elif smtp_encryption == "TLS":
        worker = smtplib.SMTP(smtp_host, smtp_port)
        worker.ehlo()
        worker.starttls()
    else:
        raise Exception("指定的SMTP加密方法不能识别")
    worker.set_debuglevel(1)
    worker.ehlo()
    worker.login(user=smtp_username, password=smtp_password)
    return worker.sendmail(
        from_addr=from_addr, to_addrs=to_addrs, msg=email.as_string()
    )
