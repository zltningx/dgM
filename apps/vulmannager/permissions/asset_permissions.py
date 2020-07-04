# -*- coding: utf-8 -*-
# author: zltningx

from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.db.models import Q


class AdminOrReadOnly(BasePermission):
    message = "没有权限"

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS or request.user.is_superuser:
            return True
        else:
            return False
