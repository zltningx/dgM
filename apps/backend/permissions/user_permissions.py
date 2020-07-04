# -*- coding: utf-8 -*-
# author: zltningx


from rest_framework.permissions import BasePermission


class IsSuperUser(BasePermission):
    message = "非超级用户"

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return False
