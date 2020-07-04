# -*- coding: utf-8 -*-
# author: zltningx


from rest_framework.serializers import ModelSerializer
from apps.backend.models import SMTPConfig


class SMTPConfigSerializer(ModelSerializer):
    class Meta:
        model = SMTPConfig
        fields = '__all__'
