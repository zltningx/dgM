# -*- coding: utf-8 -*-
# author: zltningx

from django.db import models


class SMTPConfig(models.Model):
    ENCRYPTION_METHODS = (
        ("NONE", "不加密"),
        ("SSL", "SSL加密"),
        ("TLS", "TLS加密"),
    )
    server = models.CharField('服务地址', max_length=256)
    port = models.PositiveIntegerField()
    username = models.CharField('邮箱账号', max_length=128)
    password = models.CharField('邮箱密码', max_length=128)
    encryption_method = models.CharField('加密方式', choices=ENCRYPTION_METHODS, max_length=8)
    signature = models.TextField('邮件签名', blank=True, null=False)
