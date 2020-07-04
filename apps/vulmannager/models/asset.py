# -*- coding: utf-8 -*-
# author: zltningx

from django.db import models
from apps.backend.models import User


class Asset(models.Model):
    name = models.CharField('资产名', max_length=32)
    domain = models.CharField('域名', max_length=72, blank=True, null=False)
    ip = models.GenericIPAddressField('IP')
    pics = models.ManyToManyField(User, related_name="pics")
    info = models.TextField('资产细节', blank=True, null=False)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    update_time = models.DateTimeField("更新时间", auto_now=True)


class Port(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='ports', blank=True, null=True)
    port = models.IntegerField("端口")
    service = models.CharField("服务名", max_length=128, blank=True, null=False)
    version = models.CharField("版本", max_length=72, blank=True, null=False)
    vulnerable = models.TextField("版本漏洞信息", blank=True, null=False)
    update_time = models.DateTimeField("更新时间", auto_now=True)
