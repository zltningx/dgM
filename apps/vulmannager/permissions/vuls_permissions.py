# -*- coding: utf-8 -*-
# author: zltningx

from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.db.models import Q


class VulIsEditorOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):

        # 超级 可以删除
        if request.method == 'DELETE':
            if request.user.is_superuser:
                return True
            else:
                return False

        # 审核组 安全组 可以编辑
        if (request.method in SAFE_METHODS or
                request.user.is_superuser or
                request.user.groups.filter(name='审核组') or
                request.user.groups.filter(name='安全组')):
            return True

        # 资产相关人员可以编辑
        if obj.asset.pics.all().filter(id=request.user.id):
            return True
        else:
            return False
