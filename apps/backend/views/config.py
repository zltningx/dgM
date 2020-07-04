# -*- coding: utf-8 -*-
# author: zltningx


from rest_framework.viewsets import ModelViewSet

from apps.backend.serializers import SMTPConfigSerializer
from apps.backend.models import SMTPConfig
from apps.backend.permissions import IsSuperUser


class SMTPConfigViewSet(ModelViewSet):
    permission_classes = [IsSuperUser]
    queryset = SMTPConfig.objects.all()
    serializer_class = SMTPConfigSerializer
