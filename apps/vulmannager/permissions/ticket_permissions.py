# -*- coding: utf-8 -*-
# author: zltningx


from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.db.models import Q


class TicketIsOwnerOrReadOnly(BasePermission):
    message = "你不是这个Ticket的主人"

    def has_object_permission(self, request, view, obj):

        # 审核组 安全组 可以编辑
        if (request.method in SAFE_METHODS or
                request.user.is_superuser or
                request.user.groups.filter(name='审核组') or
                request.user.groups.filter(name='安全组')):
            return True
        if obj.creator == request.user:
            if request.data['status'] > obj.status:
                # 进入流程后用户没有编辑权限
                if request.data['status'] > 1:
                    return False
                else:
                    return True
            else:
                # 用户可撤回流程
                if request.data['status'] == 0:
                    return True
                else:
                    return False
        else:
            return False
